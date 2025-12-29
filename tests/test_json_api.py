import pytest
from toon_parse import JsonConverter, AsyncJsonConverter, Encryptor
from cryptography.fernet import Fernet

@pytest.fixture
def fernet_key():
    return Fernet.generate_key()

@pytest.fixture
def encryptor(fernet_key):
    return Encryptor(key=fernet_key, algorithm='fernet')

@pytest.fixture
def converter():
    return JsonConverter()

@pytest.fixture
def secure_converter(encryptor):
    return JsonConverter(encryptor=encryptor)

@pytest.fixture
def async_converter():
    return AsyncJsonConverter()

def test_json_to_toon(converter):
    data = {"a": 1}
    toon = converter.to_toon(data)
    assert 'a: 1' in toon

def test_toon_to_json(converter):
    toon = 'a: 1'
    res = converter.from_toon(toon) 
    if isinstance(res, str):
        import json
        res = json.loads(res)
    assert res['a'] == 1

def test_json_to_xml(converter):
    data = {"root": {"item": "val"}}
    xml = converter.to_xml(data)
    assert '<root>' in xml
    assert '<item>val</item>' in xml

def test_xml_to_json(converter):
    xml = '<root><item>val</item></root>'
    res = converter.from_xml(xml)
    if isinstance(res, str):
        import json
        res = json.loads(res)
    assert 'root' in res
    assert res['root']['item'] == 'val'

def test_json_to_yaml(converter):
    data = {"a": 1}
    yaml = converter.to_yaml(data)
    assert 'a: 1' in yaml

def test_yaml_to_json(converter):
    yaml = 'a: 1'
    res = converter.from_yaml(yaml)
    if isinstance(res, str):
        import json
        res = json.loads(res)
    assert res['a'] == 1

def test_json_to_csv(converter):
    data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
    csv = converter.to_csv(data)
    assert 'a,b' in csv
    assert '1,2' in csv

def test_csv_to_json(converter):
    csv = 'a,b\n1,2'
    res = converter.from_csv(csv)
    if isinstance(res, str):
        import json
        res = json.loads(res)
    assert res[0]['a'] == 1 
    assert res[0]['b'] == 2

def test_encryption_json_hub(secure_converter, encryptor):
    # Test one flow: XML -> Encrypted JSON
    xml = '<data>secret</data>'
    enc_xml = encryptor.encrypt(xml)
    
    # Middleware: Encrypted XML -> Encrypted JSON
    res = secure_converter.from_xml(
        enc_xml, conversion_mode='middleware'
    )
    dec_res = encryptor.decrypt(res)
    assert 'data' in dec_res

@pytest.mark.asyncio
async def test_to_toon_async(async_converter):
    data = {"async": True}
    toon = await async_converter.to_toon(data)
    assert 'async: true' in toon

@pytest.mark.asyncio
async def test_from_xml_async(async_converter):
    xml = '<root>async</root>'
    res = await async_converter.from_xml(xml)
    if isinstance(res, str):
        import json
        res = json.loads(res)
    assert res['root'] == 'async'
