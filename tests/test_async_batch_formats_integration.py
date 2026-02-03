import pytest
import asyncio
from toon_parse.json_parse import AsyncBatchJsonConverter
from toon_parse.yaml_parse import AsyncBatchYamlConverter
from toon_parse.xml_parse import AsyncBatchXmlConverter
from toon_parse.csv_parse import AsyncBatchCsvConverter
from toon_parse.encrypt import Encryptor
from cryptography.fernet import Fernet


@pytest.mark.asyncio
async def test_async_batch_json_yaml_pipeline():
    """Test async batch JSON → YAML → JSON roundtrip."""
    json_converter = AsyncBatchJsonConverter()
    yaml_converter = AsyncBatchYamlConverter()
    
    json_list = [{"name": "Alice"}, {"name": "Bob"}]
    
    # JSON → YAML
    yaml_results = await json_converter.to_yaml(json_list)
    assert len(yaml_results) == 2
    
    # YAML → JSON
    json_results = await yaml_converter.to_json(yaml_results, return_json=False)
    assert len(json_results) == 2
    assert json_results[0]['name'] == 'Alice'


@pytest.mark.asyncio
async def test_async_batch_xml_json_pipeline():
    """Test async batch XML → JSON → XML roundtrip."""
    xml_converter = AsyncBatchXmlConverter()
    json_converter = AsyncBatchJsonConverter()
    
    xml_list = [
        "<user><name>Alice</name></user>",
        "<user><name>Bob</name></user>"
    ]
    
    # XML → JSON
    json_results = await xml_converter.to_json(xml_list)
    assert len(json_results) == 2
    
    # JSON → XML
    xml_results = await json_converter.to_xml(json_results)
    assert len(xml_results) == 2
    assert "<user>" in xml_results[0]


@pytest.mark.asyncio
async def test_async_batch_concurrent_multi_format():
    """Test running multiple format converters concurrently."""
    json_conv = AsyncBatchJsonConverter()
    yaml_conv = AsyncBatchYamlConverter()
    xml_conv = AsyncBatchXmlConverter()
    csv_conv = AsyncBatchCsvConverter()
    
    json_data = [{"id": 1}, {"id": 2}]
    yaml_data = ["id: 1", "id: 2"]
    xml_data = ["<item>1</item>", "<item>2</item>"]
    csv_data = ["id\n1", "id\n2"]
    
    # Run all conversions concurrently
    results = await asyncio.gather(
        json_conv.to_toon(json_data),
        yaml_conv.to_toon(yaml_data),
        xml_conv.to_toon(xml_data),
        csv_conv.to_toon(csv_data)
    )
    
    assert len(results) == 4
    for result in results:
        assert len(result) == 2


@pytest.mark.asyncio
async def test_async_batch_encrypted_cross_format():
    """Test encrypted async batch cross-format conversion."""
    key = Fernet.generate_key()
    encryptor = Encryptor(key)
    
    json_conv = AsyncBatchJsonConverter(encryptor)
    yaml_conv = AsyncBatchYamlConverter(encryptor)
    
    json_list = ['{"name": "Alice"}', '{"name": "Bob"}']
    encrypted_inputs = [encryptor.encrypt(j) for j in json_list]
    
    # JSON → YAML with encryption
    yaml_results = await json_conv.to_yaml(encrypted_inputs, conversion_mode="middleware")
    
    assert len(yaml_results) == 2
    for result in yaml_results:
        assert isinstance(result, str)


@pytest.mark.asyncio
async def test_async_batch_mixed_validation():
    """Test concurrent validation across multiple formats."""
    json_data = ['{"valid": "json"}', 'invalid']
    yaml_data = ["valid: yaml", ": invalid"]
    xml_data = ["<valid>xml</valid>", "<invalid"]
    csv_data = ["name,age\nAlice,30", "valid"]
    
    results = await asyncio.gather(
        AsyncBatchJsonConverter.validate(json_data),
        AsyncBatchYamlConverter.validate(yaml_data),
        AsyncBatchXmlConverter.validate(xml_data),
        AsyncBatchCsvConverter.validate(csv_data)
    )
    
    assert len(results) == 4
    # Each format should have 2 validation results
    for format_results in results:
        assert len(format_results) == 2


@pytest.mark.asyncio
async def test_async_batch_large_multi_format_dataset():
    """Test async batch processing with large datasets across formats."""
    json_conv = AsyncBatchJsonConverter()
    yaml_conv = AsyncBatchYamlConverter()
    
    # Generate 100 items for each format
    json_data = [{"id": i} for i in range(100)]
    yaml_data = [f"id: {i}" for i in range(100)]
    
    import time
    start = time.perf_counter()
    
    results = await asyncio.gather(
        json_conv.to_toon(json_data),
        yaml_conv.to_toon(yaml_data)
    )
    
    duration = time.perf_counter() - start
    
    assert len(results[0]) == 100
    assert len(results[1]) == 100
    # Should complete reasonably fast
    assert duration < 5.0


@pytest.mark.asyncio
async def test_async_batch_csv_json_yaml_chain():
    """Test async batch CSV → JSON → YAML conversion chain."""
    csv_conv = AsyncBatchCsvConverter()
    json_conv = AsyncBatchJsonConverter()
    yaml_conv = AsyncBatchYamlConverter()
    
    csv_list = [
        "name,age\nAlice,30",
        "name,age\nBob,25"
    ]
    
    # CSV → JSON
    json_results = await csv_conv.to_json(csv_list)
    assert len(json_results) == 2
    
    # JSON → YAML
    yaml_results = await json_conv.to_yaml(json_results)
    assert len(yaml_results) == 2


@pytest.mark.asyncio
async def test_async_batch_all_formats_to_toon():
    """Test converting all formats to TOON concurrently."""
    json_conv = AsyncBatchJsonConverter()
    yaml_conv = AsyncBatchYamlConverter()
    xml_conv = AsyncBatchXmlConverter()
    csv_conv = AsyncBatchCsvConverter()
    
    json_data = [{"name": "Alice"}]
    yaml_data = ["name: Alice"]
    xml_data = ["<person><name>Alice</name></person>"]
    csv_data = ["name\nAlice"]
    
    results = await asyncio.gather(
        json_conv.to_toon(json_data),
        yaml_conv.to_toon(yaml_data),
        xml_conv.to_toon(xml_data),
        csv_conv.to_toon(csv_data)
    )
    
    # All should produce TOON format
    for result in results:
        assert len(result) == 1
        # CSV to TOON produces different format
        assert len(result[0]) > 0
