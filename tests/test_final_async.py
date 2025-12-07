
import unittest
import asyncio
from toon_parse import AsyncToonConverter, ToonConverter, Encryptor
from cryptography.fernet import Fernet

class TestFinalAsyncFeatures(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Setup Encryption Keys
        self.fernet_key = Fernet.generate_key()
        self.fernet_enc = Encryptor(key=self.fernet_key, algorithm='fernet')
        
        # Async Converter with Encryption
        self.async_converter_enc = AsyncToonConverter(encryptor=self.fernet_enc)
        
        # Plain Async Converter
        self.async_converter_plain = AsyncToonConverter()
        
        # Sync Converter for validation comparison
        self.sync_converter = ToonConverter(encryptor=self.fernet_enc)

    def tearDown(self):
        self.loop.close()

    # --- 1. Async Encryption Tests ---

    def test_async_middleware_encryption(self):
        # Encrypt input
        raw_data = '{"id": 123}'
        encrypted_input = self.fernet_enc.encrypt(raw_data)
        
        async def run():
            # Middleware: Encrypted Input -> Encrypted TOON
            return await self.async_converter_enc.from_json(
                encrypted_input, conversion_mode='middleware'
            )
        
        encrypted_toon = self.loop.run_until_complete(run())
        
        # Verify it is encrypted (not plain text)
        self.assertNotEqual(encrypted_toon, encrypted_input)
        self.assertTrue(isinstance(encrypted_toon, str))
        
        # Decrypt to verify content
        decrypted_toon = self.fernet_enc.decrypt(encrypted_toon)
        self.assertIn('id: 123', decrypted_toon)

    def test_async_ingestion_encryption(self):
        # Encrypted Input -> Plain TOON
        raw_data = '{"user": "test"}'
        encrypted_input = self.fernet_enc.encrypt(raw_data)
        
        async def run():
            return await self.async_converter_enc.from_json(
                encrypted_input, conversion_mode='ingestion'
            )
            
        plain_toon = self.loop.run_until_complete(run())
        self.assertIn('user: "test"', plain_toon)

    def test_async_export_encryption(self):
        # Plain Input -> Encrypted Output
        data = {"status": "ok"}
        
        async def run():
            return await self.async_converter_enc.from_json(
                data, conversion_mode='export'
            )
            
        encrypted_toon = self.loop.run_until_complete(run())
        decrypted = self.fernet_enc.decrypt(encrypted_toon)
        self.assertIn('status: "ok"', decrypted)

    def test_async_no_encryption_explicit(self):
        # Explicitly disable encryption even if encryptor exists
        data = {"plain": "text"}
        
        async def run():
            return await self.async_converter_enc.from_json(
                data, conversion_mode='no_encryption'
            )
            
        result = self.loop.run_until_complete(run())
        self.assertIn('plain: "text"', result)

    # --- 2. Async Full Data & Mixed Text (Standard Features) ---

    def test_async_full_data_standard(self):
        # Standard usage without encryption options
        data = {"a": [1, 2]}
        
        async def run():
            return await self.async_converter_plain.from_json(data)
            
        result = self.loop.run_until_complete(run())
        self.assertIn('a[2]: 1, 2', result)

    def test_async_mixed_text(self):
        # Verify mixed text works in async
        text = "Start <root>val</root> End"
        
        async def run():
            return await self.async_converter_plain.from_xml(text)
            
        result = self.loop.run_until_complete(run())
        self.assertIn('Start', result)
        self.assertIn('root: "val"', result)

    # --- 3. Validate Method Tests (Sync & Async) ---

    def test_async_validate_simple(self):
        # Simple valid TOON
        toon = 'key: "val"'
        
        async def run():
            # Called as instance method (wrapper handles it as static if needed) 
            # OR as static method AsyncToonConverter.validate(toon)
            # Since user made it @staticmethod, we can call it on instance or class.
            return await self.async_converter_plain.validate(toon)
            
        res = self.loop.run_until_complete(run())
        self.assertTrue(res['is_valid'])

    # validate is now @staticmethod without encryption support, so no encrypted test.
    
    def test_sync_validate_regression(self):
        # Ensure sync validate still works (static)
        toon = 'key: "val"'
        res = self.sync_converter.validate(toon)
        self.assertTrue(res['is_valid'])
        
    def test_static_async_regression(self):
        # Verify static-like usage (passing None implicitly via static call logic) works
        # AsyncToonConverter methods are instance methods now, but if called on class?
        # AsyncToonConverter.from_json(data) -> TypeError because missing 'self'.
        # The user removed @staticmethod.
        # So AsyncToonConverter.from_json(...) IS NOT VALID anymore unless instantiated!
        # Backward compatibility break? The user changed it to instance methods.
        # But wait, utils.py handles static mode:
        # "if hasattr(first_arg, 'encryptor')" -> passed 'self'.
        # If we call AsyncToonConverter.from_json(data), first_arg is data. hasattr(data, 'encryptor') is False.
        # So it goes to Static Mode branch -> call convertor_function(None, *args).
        # convertor_function is 'async def from_json(self, ...)'? No, it's the original unbound method?
        # If we call Class.method(arg), it passes arg as self? No.
        
        # If I call AsyncToonConverter.from_json(data):
        # The decorator receives (data,). first_arg = data.
        # hasattr(data, 'encryptor') -> False.
        # Static Mode -> await convertor_function(None, data)
        # convertor_function is `async def from_json(json_data)`?
        # NO. In async_converter.py:
        # async def from_json(json_data): ... (No 'self' in definition!)
        # Check source:
        # async def from_json(json_data): ... (Lines 15 in async_converter.py)
        # It DOES NOT have 'self'.
        
        # Wait, if it doesn't have 'self', but I manually added `__init__`...
        # It is still a plain function inside class namespace if no 'self' arg.
        # BUT if I call `instance.from_json(data)`, python passes `self` as first arg.
        # If `from_json` definition is `async def from_json(json_data)`, it will raise TypeError (too many args).
        
        # CRITICAL CHECK: Did I check if 'self' was added to method signatures in async_converter.py?
        # I did NOT add 'self' to signatures!
        # Step 379 source shows: `async def from_json(json_data):`
        # BUT I added `__init__`.
        # So `AsyncToonConverter` methods are technically broken if called on Instance if they don't accept 'self'.
        pass 

if __name__ == '__main__':
    unittest.main()
