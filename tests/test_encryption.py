
import unittest
from toon_parse import ToonConverter, Encryptor
from cryptography.fernet import Fernet
import base64

class TestEncryptionIntegration(unittest.TestCase):
    
    def setUp(self):
        # Fernet Setup
        self.fernet_key = Fernet.generate_key()
        self.fernet_enc = Encryptor(key=self.fernet_key, algorithm='fernet')
        self.fernet_converter = ToonConverter(encryptor=self.fernet_enc)

        # Base64 Setup (Simple verification)
        self.base64_enc = Encryptor(algorithm='base64')
        self.base64_converter = ToonConverter(encryptor=self.base64_enc)
        
        # Plain Converter (No encryption)
        self.plain_converter = ToonConverter()

        self.sample_data = {"name": "Alice", "role": "admin"}
        self.sample_toon = 'name: "Alice"\nrole: "admin"'
        self.mixed_text = 'Check this: {"user": "Bob"}. End.'
        self.expected_mixed_toon = 'Check this:\nuser: "Bob"\n. End.'

    # --- 1. Middleware Mode (Enc -> Enc) ---
    def test_middleware_fernet(self):
        # Encrypt input manually
        raw_json_str = '{"name": "Alice", "role": "admin"}'
        encrypted_input = self.fernet_enc.encrypt(raw_json_str)
        
        # Convert middleware
        encrypted_output = self.fernet_converter.from_json(
            encrypted_input, conversion_mode='middleware'
        )
        
        # Verify output is encrypted different string (IV changes) but decrypts to correct TOON
        self.assertNotEqual(encrypted_output, encrypted_input)
        decrypted_toon = self.fernet_enc.decrypt(encrypted_output)
        
        # Simple check for content in TOON format
        self.assertIn('name: "Alice"', decrypted_toon)
        self.assertIn('role: "admin"', decrypted_toon)

    def test_middleware_base64_mixed(self):
        # Base64 is deterministic, easier to check exact strings
        # Input mixed text encrypted
        plain_mixed = 'Msg: {"a": 1}'
        enc_input = base64.b64encode(plain_mixed.encode()).decode()
        
        # Middleware convert
        result_enc = self.base64_converter.from_json(
            enc_input, conversion_mode='middleware'
        )
        
        # Decrypt result
        result_plain = base64.b64decode(result_enc).decode()
        self.assertIn('a: 1', result_plain)

    # --- 2. Ingestion Mode (Enc -> Plain) ---
    def test_ingestion_mode(self):
        # Encrypted JSON -> Plain TOON
        raw_str = '{"x": 100}'
        enc_input = self.fernet_enc.encrypt(raw_str)
        
        # Conversion mode 'ingestion' should return plain TOON string
        result_toon = self.fernet_converter.from_json(
            enc_input, conversion_mode='ingestion'
        )
        
        self.assertIn('x: 100', result_toon)
        # Should NOT decrypt cleanly as fernet (it is plain text)
        with self.assertRaises(Exception):
            self.fernet_enc.decrypt(result_toon)

    # --- 3. Export Mode (Plain -> Enc) ---
    def test_export_mode(self):
        # Plain JSON/Dict -> Encrypted TOON
        result_enc = self.fernet_converter.from_json(
            self.sample_data, conversion_mode='export'
        )
        
        # It should be encrypted
        decrypted = self.fernet_enc.decrypt(result_enc)
        self.assertIn('name: "Alice"', decrypted)

    def test_export_to_json_encrypted(self):
        # Plain TOON -> Encrypted JSON
        enc_json = self.fernet_converter.to_json(
            self.sample_toon, conversion_mode='export', return_json=True
        )
        decrypted = self.fernet_enc.decrypt(enc_json)
        self.assertIn('"name": "Alice"', decrypted)

    # --- 4. No Encryption / Existing Functionality ---
    def test_no_encryption_explicit(self):
        # Using encrypted converter but conversion_mode='no_encryption'
        result = self.fernet_converter.from_json(
            self.sample_data, conversion_mode='no_encryption'
        )
        self.assertIn('name: "Alice"', result)
        # Verify it's NOT encrypted
        self.assertFalse(result.startswith('gAAAA')) # Fernet prefix roughly

    def test_legacy_full_data_sync(self):
        # Test standard converter without encryptor
        result = self.plain_converter.from_json(self.sample_data)
        self.assertIn('name: "Alice"', result)
        
        # Round trip
        back_to_json = self.plain_converter.to_json(result)
        # to_json returns dict/list by default if return_json=False is not set? 
        # Wait, default signature: to_json(toon_string, return_json=True) -> string
        import json
        decoded = json.loads(back_to_json)
        self.assertEqual(decoded['name'], 'Alice')

    def test_legacy_mixed_text_sync(self):
        result = self.plain_converter.from_json(self.mixed_text)
        self.assertIn('Check this:', result)
        self.assertIn('user: "Bob"', result)

    # --- 5. Error Handling ---
    def test_error_return_json_false_export(self):
        # Export mode requires return_json=True (string output) to encrypt
        with self.assertRaises(ValueError):
            self.fernet_converter.to_json(
                self.sample_toon, 
                return_json=False, 
                conversion_mode='export'
            )

    # --- 6. Static Compatibility ---
    def test_static_usage_regression(self):
        # Verify that calling methods statically still works (skips encryption)
        data = {"static": "check"}
        # Calling directly on class, not instance
        result = ToonConverter.from_json(data)
        self.assertIn('static: "check"', result)
        
        # Backward check
        json_out = ToonConverter.to_json(result)
        self.assertIn('"static": "check"', json_out)

    def test_arg_edge_cases(self):
        # 1. Positional conversion_mode
        # from_json(self, json_data, conversion_mode=...)
        # passing ("data", "export")
        data = {"foo": "bar"}
        # Expect encrypted output
        result = self.fernet_converter.from_json(data, "export")
        self.assertNotEqual(result, data)
        self.assertTrue(isinstance(result, str))
        decrypted = self.fernet_converter.encryptor.decrypt(result)
        self.assertIn('foo: "bar"', decrypted)

        # 2. Keyword arg for data in Instance Mode
        # from_json(json_data=...)
        res_kw = self.fernet_converter.from_json(json_data=data, conversion_mode="export")
        dec_kw = self.fernet_converter.encryptor.decrypt(res_kw)
        self.assertIn('foo: "bar"', dec_kw)

if __name__ == '__main__':
    unittest.main()
