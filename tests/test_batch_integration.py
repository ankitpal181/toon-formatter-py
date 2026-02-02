import pytest
import os
import tempfile
from toon_parse.batch_converter import BatchToonConverter
from toon_parse.encrypt import Encryptor
from cryptography.fernet import Fernet

@pytest.fixture
def fernet_key():
    return Fernet.generate_key()

@pytest.fixture
def encryptor(fernet_key):
    return Encryptor(key=fernet_key, algorithm='fernet')

def test_encrypted_batch_middleware(encryptor):
    """
    Scenario: Encrypted List of JSONs -> Decrypt -> Convert -> Encrypt -> List of TOONs
    """
    raw_data = ['{"id": 1}', '{"id": 2}']
    encrypted_inputs = [encryptor.encrypt(item) for item in raw_data]
    
    converter = BatchToonConverter(encryptor=encryptor)
    
    # Process batch with middleware mode
    encrypted_results = converter.from_json(encrypted_inputs, conversion_mode="middleware")
    
    assert isinstance(encrypted_results, list)
    assert len(encrypted_results) == 2
    
    # Decrypt and verify
    decrypted_1 = encryptor.decrypt(encrypted_results[0])
    decrypted_2 = encryptor.decrypt(encrypted_results[1])
    
    assert 'id: 1' in decrypted_1
    assert 'id: 2' in decrypted_2

def test_encrypted_file_processing(encryptor):
    """
    Scenario: Encrypted File Content -> Decrypt -> Convert -> Encrypt -> Single Encrypted String
    """
    raw_content = '{"user": "secure"}'
    encrypted_content = encryptor.encrypt(raw_content)
    
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        # We write the encrypted string to file. 
        # Note: encryptor.encrypt returns string (base64 encoded bytes usually).
        tmp.write(encrypted_content)
        tmp_path = tmp.name
        
    try:
        converter = BatchToonConverter(encryptor=encryptor)
        
        # Result should be an encrypted string containing the converted TOON
        result = converter.from_json(tmp_path, conversion_mode="middleware")
        
        assert isinstance(result, str)
        
        # Decrypt to check content
        decrypted = encryptor.decrypt(result)
        assert 'user: "secure"' in decrypted
        
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
