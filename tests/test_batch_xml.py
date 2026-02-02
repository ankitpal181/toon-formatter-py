import pytest
from toon_parse.xml_parse import BatchXmlConverter

def test_batch_xml_from_toon():
    """Verify BatchXmlConverter.from_toon with multiple items."""
    # Use standard TOON format
    toon_data = ['root: { item: "val1" }', 'root: { item: "val2" }']
    results = BatchXmlConverter.from_toon(toon_data)
    assert len(results) == 2
    assert 'item' in results[0]
    assert 'val1' in results[0]

def test_batch_xml_to_toon():
    """Verify BatchXmlConverter.to_toon with multiple items."""
    xml_data = ['<root><id>1</id></root>', '<root><id>2</id></root>']
    results = BatchXmlConverter.to_toon(xml_data)
    assert len(results) == 2
    assert "id" in results[0]
    assert "1" in results[0]

def test_batch_xml_parallel():
    """Verify parallel execution in BatchXmlConverter."""
    xml_data = ['<root><id>1</id></root>', '<root><id>2</id></root>', '<root><id>3</id></root>']
    results = BatchXmlConverter.to_toon(xml_data, parallel=True)
    assert len(results) == 3
    assert any("id" in r and "1" in r for r in results)

def test_batch_xml_validate():
    """Verify BatchXmlConverter.validate."""
    xml_list = ['<root><item>val</item></root>', '<root>invalid']
    results = BatchXmlConverter.validate(xml_list)
    assert len(results) == 2
    assert results[0]['is_valid'] is True
    assert results[1]['is_valid'] is False

def test_batch_xml_cross_format():
    """Verify cross-format methods in BatchXmlConverter."""
    json_data_list = ['{"id": 1}', '{"id": 2}']
    # to_json (XML data to JSON list)
    xml_data = ['<root><id>1</id></root>', '<root><id>2</id></root>']
    json_results = BatchXmlConverter.to_json(xml_data)
    # The return depends on whether toon-converter-py's xml_to_json returns dict or string
    # Assuming it returns string by default or we can check type
    assert len(json_results) == 2
    
    # from_json (JSON string to XML string list)
    xml_results = BatchXmlConverter.from_json(json_data_list)
    assert len(xml_results) == 2
    assert '<id>1</id>' in xml_results[0]
