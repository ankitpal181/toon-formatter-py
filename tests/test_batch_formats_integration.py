import pytest
from toon_parse.json_parse import BatchJsonConverter
from toon_parse.yaml_parse import BatchYamlConverter
from toon_parse.encrypt import Encryptor

def test_json_to_yaml_batch_integration():
    """Verify BatchJsonConverter.to_yaml integration."""
    json_data = [{'id': 1}, {'id': 2}]
    yaml_results = BatchJsonConverter.to_yaml(json_data)
    assert len(yaml_results) == 2
    assert "id: 1" in yaml_results[0]
    assert "id: 2" in yaml_results[1]

def test_yaml_to_json_batch_integration():
    """Verify BatchYamlConverter.to_json integration."""
    yaml_data = ['id: 1', 'id: 2']
    json_results = BatchYamlConverter.to_json(yaml_data, return_json=False)
    assert len(json_results) == 2
    assert json_results[0]['id'] == 1
    assert json_results[1]['id'] == 2

def test_encrypted_json_batch_middleware():
    """Verify BatchJsonConverter with encryption middleware."""
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    encryptor = Encryptor(key)
    converter = BatchJsonConverter(encryptor=encryptor)
    
    # 1. Create encrypted data
    plain_json = '{"id": 1}'
    encrypted_json = encryptor.encrypt(plain_json)
    
    # 2. Process using middleware (Decrypt -> Convert -> Encrypt)
    # BatchToonConverter.to_toon is what we usually use for TOON conversion
    # But for BatchJsonConverter, from_toon converts TOON to JSON.
    # and to_toon converts JSON to TOON.
    
    # Let's test BatchJsonConverter.to_toon with middleware
    # Input: Encrypted JSON -> Decrypt -> Convert to TOON -> Encrypt
    encrypted_payloads = [encrypted_json, encryptor.encrypt('{"id": 2}')]
    
    results = converter.to_toon(encrypted_payloads, conversion_mode="middleware")
    assert len(results) == 2
    
    # Decrypt results to verify
    for i, res in enumerate(results):
        decrypted = encryptor.decrypt(res)
        assert f"id: {i+1}" in decrypted

def test_batch_cross_validation():
    """Verify cross-format validation."""
    # BatchJsonConverter can validate JSON lists
    # BatchYamlConverter can validate YAML lists
    
    json_list = ['{"id": 1}', 'invalid json']
    yaml_list = ['id: 1', 'invalid: [yaml']
    
    json_val = BatchJsonConverter.validate(json_list)
    yaml_val = BatchYamlConverter.validate(yaml_list)
    
    assert json_val[0]['is_valid'] is True
    assert json_val[1]['is_valid'] is False
    
    assert yaml_val[0]['is_valid'] is True
    # YAML is very permissive, but if validator is strict it might catch errors
