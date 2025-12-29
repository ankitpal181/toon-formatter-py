import pytest
from toon_parse.encrypt import Encryptor
from cryptography.fernet import Fernet
import base64

@pytest.fixture
def fernet_enc():
    key = Fernet.generate_key()
    return Encryptor(key=key, algorithm='fernet')

@pytest.fixture
def xor_enc():
    return Encryptor(key='secret', algorithm='xor')

@pytest.fixture
def b64_enc():
    return Encryptor(algorithm='base64')

def test_fernet_encrypt_decrypt(fernet_enc):
    data = "Secret Data"
    encrypted = fernet_enc.encrypt(data)
    assert data != encrypted
    decrypted = fernet_enc.decrypt(encrypted)
    assert data == decrypted

def test_xor_encrypt_decrypt(xor_enc):
    data = "Secret Data"
    encrypted = xor_enc.encrypt(data)
    assert data != encrypted
    decrypted = xor_enc.decrypt(encrypted)
    assert data == decrypted

def test_base64_encrypt_decrypt(b64_enc):
    data = "Secret Data"
    encrypted = b64_enc.encrypt(data)
    expected = base64.b64encode(data.encode()).decode()
    assert encrypted == expected
    decrypted = b64_enc.decrypt(encrypted)
    assert data == decrypted

def test_errors():
    with pytest.raises(ValueError):
        Encryptor(algorithm='fernet') # No key
        
    enc = Encryptor(algorithm='invalid')
    with pytest.raises(ValueError):
        enc.encrypt("data")
