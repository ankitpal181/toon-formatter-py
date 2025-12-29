import pytest
import asyncio
from toon_parse import ToonConverter, AsyncToonConverter, Encryptor
from cryptography.fernet import Fernet

@pytest.fixture
def fernet_key():
    return Fernet.generate_key()

@pytest.fixture
def encryptor(fernet_key):
    return Encryptor(key=fernet_key, algorithm='fernet')

@pytest.fixture
def secure_converter(encryptor):
    return ToonConverter(encryptor=encryptor)

@pytest.fixture
def secure_async_converter(encryptor):
    return AsyncToonConverter(encryptor=encryptor)

def test_json_to_toon_basic():
    data = {"name": "Alice", "age": 30}
    # Static
    toon = ToonConverter.from_json(data)
    assert 'name: "Alice"' in toon
    assert 'age: 30' in toon
    
    # Round trip
    back = ToonConverter.to_json(toon)
    if isinstance(back, str):
        import json
        back = json.loads(back)
    assert back == data

def test_mixed_text_support():
    text = 'Content: {"a": 1} End'
    toon = ToonConverter.from_json(text)
    assert 'Content:' in toon
    assert 'a: 1' in toon

def test_encryption_middleware(secure_converter, encryptor):
    # Middleware: Encrypted -> Encrypted
    raw = '{"secret": "value"}'
    encrypted_input = encryptor.encrypt(raw)
    
    result = secure_converter.from_json(
        encrypted_input, conversion_mode="middleware"
    )
    decrypted = encryptor.decrypt(result)
    assert 'secret: "value"' in decrypted

def test_encryption_ingestion(secure_converter, encryptor):
    # Ingestion: Encrypted -> Plain
    raw = '{"secret": "value"}'
    encrypted_input = encryptor.encrypt(raw)
    
    result = secure_converter.from_json(
        encrypted_input, conversion_mode="ingestion"
    )
    assert 'secret: "value"' in result

def test_encryption_export(secure_converter, encryptor):
    # Export: Plain -> Encrypted TOON
    data = {"secret": "value"}
    result = secure_converter.from_json(
        data, conversion_mode="export"
    )
    decrypted = encryptor.decrypt(result)
    assert 'secret: "value"' in decrypted

def test_to_json_encryption(secure_converter, encryptor):
    # TOON -> Encrypted JSON
    toon = 'secret: "value"'
    result = secure_converter.to_json(
        toon, conversion_mode="export", return_json=True
    )
    decrypted = encryptor.decrypt(result)
    assert '"secret": "value"' in decrypted

@pytest.mark.asyncio
async def test_from_json_async():
    converter = AsyncToonConverter()
    data = {"name": "Alice"}
    toon = await converter.from_json(data)
    assert 'name: "Alice"' in toon

@pytest.mark.asyncio
async def test_to_json_async():
    converter = AsyncToonConverter()
    toon = 'name: "Alice"'
    data = await converter.to_json(toon)
    if isinstance(data, str):
        import json
        data = json.loads(data)
    assert data['name'] == 'Alice'

@pytest.mark.asyncio
async def test_encryption_async(secure_async_converter, encryptor):
    raw = '{"secret": "async"}'
    encrypted_input = encryptor.encrypt(raw)
    
    result = await secure_async_converter.from_json(
        encrypted_input, conversion_mode="middleware"
    )
    decrypted = encryptor.decrypt(result)
    assert 'secret: "async"' in decrypted
