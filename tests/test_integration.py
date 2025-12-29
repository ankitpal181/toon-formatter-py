import pytest
import asyncio
import json
from toon_parse import (
    ToonConverter, AsyncToonConverter, 
    JsonConverter, AsyncJsonConverter,
    XmlConverter, AsyncXmlConverter,
    YamlConverter, AsyncYamlConverter,
    CsvConverter, AsyncCsvConverter,
    Encryptor, parse_value
)
from cryptography.fernet import Fernet

@pytest.fixture
def fernet_key():
    return Fernet.generate_key()

@pytest.fixture
def encryptor(fernet_key):
    return Encryptor(key=fernet_key, algorithm='fernet')

def test_format_chaining_round_trip():
    """
    Scenario: dict -> JSON -> TOON -> XML -> YAML -> JSON -> dict
    Verification: Types might stringify through XML, so we use parse_value if needed.
    """
    original_data = {"root": {"user": "Alice", "meta": {"id": 1, "active": True}}}
    
    # 1. JSON (string)
    json_str = json.dumps(original_data)
    
    # 2. TOON
    toon = ToonConverter.from_json(json_str)
    assert 'user: "Alice"' in toon
    
    # 3. XML
    xml = ToonConverter.to_xml(toon)
    assert '<root>' in xml
    assert '<user>Alice</user>' in xml
    
    # 4. YAML
    yaml_out = XmlConverter().to_yaml(xml)
    assert 'user: Alice' in yaml_out
    
    # 5. JSON string back
    res = YamlConverter().to_json(yaml_out)
    if isinstance(res, str):
        res = json.loads(res)
    
    # The package xml_to_json doesn't auto-parse primitives, so they stay as strings
    assert res['root']['user'] == "Alice"
    # Allow either bool or string representation if it went through XML
    active_val = res['root']['meta']['active']
    assert str(active_val).lower() == "true"

def test_secure_global_middleware(encryptor):
    """
    Scenario: Encrypted JSON -> Decrypted TOON (Ingestion) -> Encrypted XML (Export)
    """
    raw_json = '{"root": {"secret": "integration"}}'
    encrypted_json = encryptor.encrypt(raw_json)
    
    # 1. Decrypted TOON (Ingestion)
    toon_conv = ToonConverter(encryptor=encryptor)
    plain_toon = toon_conv.from_json(encrypted_json, conversion_mode="ingestion")
    assert 'secret: "integration"' in plain_toon
    
    # 2. Encrypted XML (Export from plain TOON)
    xml_conv = XmlConverter(encryptor=encryptor)
    encrypted_xml = xml_conv.from_toon(plain_toon, conversion_mode="export")
    
    # Verify XML
    decrypted_xml = encryptor.decrypt(encrypted_xml)
    assert '<secret>integration</secret>' in decrypted_xml

def test_complex_mixed_text_processing():
    """
    Scenario: Mixed text with JSON, XML, and CSV blocks
    """
    mixed_text = "JSON: {\"id\": 1} XML: <meta>v1</meta> CSV: col1,col2\nval1,val2"
    
    # 1. End-to-end extraction (using ToonConverter hub)
    # Applying them sequentially or mixed
    # ToonConverter.from_json finds JSON, etc.
    res = ToonConverter.from_json(mixed_text)
    res = ToonConverter.from_xml(res)
    res = ToonConverter.from_csv(res)
    
    assert 'id: 1' in res
    assert 'meta: "v1"' in res
    assert 'col1,col2' in res
    assert 'JSON:' in res

def test_nested_data_csv_flattening():
    """
    Scenario: List -> TOON -> CSV (Flattened) -> JSON -> dict
    """
    nested_data = [
        {"id": 101, "profile": {"name": "Alice"}},
        {"id": 102, "profile": {"name": "Bob"}}
    ]
    
    # 1. TOON
    toon = ToonConverter.from_json(nested_data)
    
    # 2. CSV
    csv_str = ToonConverter.to_csv(toon)
    assert 'profile.name' in csv_str
    
    # 3. JSON back
    json_res = CsvConverter().to_json(csv_str)
    if isinstance(json_res, str):
        json_res = json.loads(json_res)
    
    assert json_res[0]['profile']['name'] == 'Alice'

@pytest.mark.asyncio
async def test_async_multi_hop_conversion():
    """
    Scenario: Async JSON -> Async TOON -> Async XML -> Async YAML
    """
    async_conv = AsyncToonConverter()
    data = {"root": {"async": True, "hops": 3}}
    
    # 1. JSON -> TOON
    toon = await async_conv.from_json(data)
    
    # 2. TOON -> XML
    xml = await async_conv.to_xml(toon)
    
    # 3. XML -> YAML
    yaml_conv = AsyncYamlConverter()
    yaml_out = await yaml_conv.from_xml(xml)
    
    # XML to YAML often stringifies tags like <hops>3</hops> to hops: '3'
    assert 'hops:' in yaml_out
    assert '3' in yaml_out
    assert 'async:' in yaml_out
