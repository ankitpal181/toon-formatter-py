import pytest
from toon_parse import YamlConverter, AsyncYamlConverter

@pytest.fixture
def converter():
    return YamlConverter()

@pytest.fixture
def async_converter():
    return AsyncYamlConverter()

def test_yaml_to_json(converter):
    yaml_str = "key: value"
    res = converter.to_json(yaml_str)
    if isinstance(res, str):
        import json
        res = json.loads(res)
    assert res['key'] == 'value'

def test_json_to_yaml(converter):
    data = {"key": "value"}
    yaml = converter.from_json(data)
    assert "key: value" in yaml

def test_yaml_to_toon(converter):
    yaml_str = "key: value"
    toon = converter.to_toon(yaml_str)
    assert 'key: "value"' in toon

def test_toon_to_yaml(converter):
    toon = 'key: "value"'
    yaml = converter.from_toon(toon)
    assert "key: value" in yaml

# XML/CSV interop via YAML hub
def test_yaml_to_xml(converter):
    yaml_str = "root:\n  item: value"
    xml = converter.to_xml(yaml_str)
    assert '<root>' in xml
    assert 'value' in xml

@pytest.mark.asyncio
async def test_to_json_async(async_converter):
    yaml_str = "async: true"
    res = await async_converter.to_json(yaml_str)
    if isinstance(res, str):
        import json
        res = json.loads(res)
    assert res['async'] is True
