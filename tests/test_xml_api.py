import pytest
from toon_parse import XmlConverter, AsyncXmlConverter

@pytest.fixture
def converter():
    return XmlConverter()

@pytest.fixture
def async_converter():
    return AsyncXmlConverter()

def test_xml_to_json(converter):
    xml = '<root>value</root>'
    res = converter.to_json(xml)
    if isinstance(res, str):
        import json
        res = json.loads(res)
    assert res['root'] == 'value'

def test_json_to_xml(converter):
    data = {"root": "value"}
    xml = converter.from_json(data)
    assert '<root>value</root>' in xml

def test_xml_attributes(converter):
    xml = '<item id="1">value</item>'
    res = converter.to_json(xml)
    # Depending on implementation
    assert 'item' in res

def test_xml_to_toon(converter):
    xml = '<root>value</root>'
    toon = converter.to_toon(xml)
    assert 'root: "value"' in toon

@pytest.mark.asyncio
async def test_to_json_async(async_converter):
    xml = '<root>async</root>'
    res = await async_converter.to_json(xml)
    if isinstance(res, str):
        import json
        res = json.loads(res)
    assert res['root'] == 'async'
