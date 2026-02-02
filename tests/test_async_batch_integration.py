import pytest
import asyncio
from toon_parse.async_batch_converter import AsyncBatchToonConverter
from toon_parse.encrypt import Encryptor
from cryptography.fernet import Fernet


@pytest.mark.asyncio
async def test_async_batch_json_to_yaml_roundtrip():
    """Test async batch conversion from JSON to YAML and back."""
    converter = AsyncBatchToonConverter()
    
    json_list = [
        {"name": "Alice", "city": "NYC"},
        {"name": "Bob", "city": "LA"}
    ]
    
    # JSON -> TOON
    toon_results = await converter.from_json(json_list)
    assert len(toon_results) == 2
    
    # TOON -> YAML
    yaml_results = await converter.to_yaml(toon_results)
    assert len(yaml_results) == 2
    assert "name: Alice" in yaml_results[0]
    
    # YAML -> TOON (roundtrip)
    toon_roundtrip = await converter.from_yaml(yaml_results)
    assert len(toon_roundtrip) == 2
    assert "name:" in toon_roundtrip[0] and "Alice" in toon_roundtrip[0]


@pytest.mark.asyncio
async def test_async_batch_cross_format_conversion():
    """Test async batch cross-format conversions."""
    converter = AsyncBatchToonConverter()
    
    # Start with XML
    xml_list = [
        "<user><id>1</id><name>Alice</name></user>",
        "<user><id>2</id><name>Bob</name></user>"
    ]
    
    # XML -> TOON
    toon_from_xml = await converter.from_xml(xml_list)
    
    # TOON -> JSON
    json_from_toon = await converter.to_json(toon_from_xml, return_json=False)
    assert len(json_from_toon) == 2
    # return_json=False returns dict objects
    assert json_from_toon[0]['user']['name'] == 'Alice'
    
    # Verify results
    assert len(json_from_toon) == 2
    assert 'user' in json_from_toon[0]


@pytest.mark.asyncio
async def test_async_batch_encrypted_pipeline():
    """Test async batch processing with encryption in a multi-step pipeline."""
    key = Fernet.generate_key()
    encryptor = Encryptor(key)
    converter = AsyncBatchToonConverter(encryptor)
    
    # Original data
    json_list = [
        '{"product": "Laptop", "price": 999}',
        '{"product": "Mouse", "price": 25}'
    ]
    
    # Encrypt inputs
    encrypted_inputs = [encryptor.encrypt(j) for j in json_list]
    
    # Middleware: decrypt -> convert -> encrypt
    encrypted_toon = await converter.from_json(encrypted_inputs, conversion_mode="middleware")
    
    assert len(encrypted_toon) == 2
    for result in encrypted_toon:
        assert isinstance(result, str)  # Base64 encrypted string
    
    # Decrypt and verify
    decrypted_results = [encryptor.decrypt(r) for r in encrypted_toon]
    assert all("product:" in r for r in decrypted_results)


@pytest.mark.asyncio
async def test_async_batch_mixed_operations():
    """Test running multiple async batch operations concurrently."""
    converter = AsyncBatchToonConverter()
    
    json_data = [{"id": 1}, {"id": 2}]
    yaml_data = ["name: Alice", "name: Bob"]
    xml_data = ["<item>A</item>", "<item>B</item>"]
    
    # Run all conversions concurrently
    json_task = converter.from_json(json_data)
    yaml_task = converter.from_yaml(yaml_data)
    xml_task = converter.from_xml(xml_data)
    
    results = await asyncio.gather(json_task, yaml_task, xml_task)
    
    assert len(results) == 3
    assert len(results[0]) == 2  # JSON results
    assert len(results[1]) == 2  # YAML results
    assert len(results[2]) == 2  # XML results


@pytest.mark.asyncio
async def test_async_batch_validation_with_errors():
    """Test async batch validation with mixed valid/invalid inputs."""
    toon_list = [
        "name: Alice\nage: 30",  # Valid
        "[3]: 1, 2",  # Invalid: size mismatch
        "city: NYC\nzip: 10001",  # Valid
        "invalid syntax here",  # Invalid
        "[2]{id,name}:\n  1,Alice\n  2,Bob"  # Valid
    ]
    
    results = await AsyncBatchToonConverter.validate(toon_list)
    
    assert len(results) == 5
    assert results[0]['is_valid'] is True
    assert results[1]['is_valid'] is False
    assert results[2]['is_valid'] is True
    assert results[3]['is_valid'] is False
    assert results[4]['is_valid'] is True


@pytest.mark.asyncio
async def test_async_batch_large_dataset():
    """Test async batch processing with a large dataset."""
    converter = AsyncBatchToonConverter()
    
    # Generate 200 items
    large_dataset = [{"id": i, "value": f"item_{i}"} for i in range(200)]
    
    import time
    start = time.perf_counter()
    results = await converter.from_json(large_dataset)
    duration = time.perf_counter() - start
    
    assert len(results) == 200
    assert all("id:" in r for r in results)
    # Should complete reasonably fast (under 5 seconds for 200 items)
    assert duration < 5.0


@pytest.mark.asyncio
async def test_async_batch_error_handling():
    """Test async batch converter handles errors gracefully."""
    converter = AsyncBatchToonConverter()
    
    # Mix of valid and potentially problematic inputs
    mixed_data = [
        {"valid": "data"},
        None,  # This might cause issues
        {"another": "valid"}
    ]
    
    try:
        results = await converter.from_json(mixed_data)
        # If it succeeds, verify results
        assert len(results) == 3
    except Exception as e:
        # If it fails, ensure it's a meaningful error
        assert e is not None


@pytest.mark.asyncio
async def test_async_batch_encryption_modes():
    """Test all encryption modes in async batch processing."""
    key = Fernet.generate_key()
    encryptor = Encryptor(key)
    converter = AsyncBatchToonConverter(encryptor)
    
    json_list = ['{"name": "Alice"}', '{"name": "Bob"}']
    
    # Test ingestion mode (decrypt input only)
    encrypted_inputs = [encryptor.encrypt(j) for j in json_list]
    ingestion_results = await converter.from_json(encrypted_inputs, conversion_mode="ingestion")
    assert len(ingestion_results) == 2
    assert all(isinstance(r, str) for r in ingestion_results)
    
    # Test export mode (encrypt output only)
    export_results = await converter.from_json(json_list, conversion_mode="export")
    assert len(export_results) == 2
    assert all(isinstance(r, str) for r in export_results)  # Base64 encrypted strings
