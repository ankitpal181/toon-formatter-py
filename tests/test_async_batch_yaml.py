import pytest
import asyncio
from toon_parse.yaml_parse import AsyncBatchYamlConverter
from toon_parse.encrypt import Encryptor
from cryptography.fernet import Fernet


@pytest.mark.asyncio
async def test_async_batch_yaml_to_toon():
    """Test async batch conversion from YAML to TOON."""
    converter = AsyncBatchYamlConverter()
    yaml_list = [
        "name: Alice\nage: 30",
        "name: Bob\nage: 25"
    ]
    
    results = await converter.to_toon(yaml_list)
    
    assert len(results) == 2
    assert "name:" in results[0]
    assert "Alice" in results[0]


@pytest.mark.asyncio
async def test_async_batch_yaml_from_toon():
    """Test async batch conversion from TOON to YAML."""
    converter = AsyncBatchYamlConverter()
    toon_list = [
        "name: Alice\nage: 30",
        "name: Bob\nage: 25"
    ]
    
    results = await converter.from_toon(toon_list)
    
    assert len(results) == 2
    assert "name:" in results[0]
    assert "Alice" in results[0]


@pytest.mark.asyncio
async def test_async_batch_yaml_to_json():
    """Test async batch YAML to JSON conversion."""
    converter = AsyncBatchYamlConverter()
    yaml_list = ["city: NYC", "city: LA"]
    
    results = await converter.to_json(yaml_list, return_json=False)
    
    assert len(results) == 2
    assert results[0]['city'] == 'NYC'


@pytest.mark.asyncio
async def test_async_batch_yaml_from_json():
    """Test async batch JSON to YAML conversion."""
    converter = AsyncBatchYamlConverter()
    json_list = [{"city": "NYC"}, {"city": "LA"}]
    
    results = await converter.from_json(json_list)
    
    assert len(results) == 2
    assert "city:" in results[0]


@pytest.mark.asyncio
async def test_async_batch_yaml_to_xml():
    """Test async batch YAML to XML conversion."""
    converter = AsyncBatchYamlConverter()
    yaml_list = ["user:\n  name: Alice", "user:\n  name: Bob"]
    
    results = await converter.to_xml(yaml_list)
    
    assert len(results) == 2
    assert "<user>" in results[0]


@pytest.mark.asyncio
async def test_async_batch_yaml_from_xml():
    """Test async batch XML to YAML conversion."""
    converter = AsyncBatchYamlConverter()
    xml_list = ["<user><name>Alice</name></user>", "<user><name>Bob</name></user>"]
    
    results = await converter.from_xml(xml_list)
    
    assert len(results) == 2
    assert "user:" in results[0]


@pytest.mark.asyncio
async def test_async_batch_yaml_to_csv():
    """Test async batch YAML to CSV conversion."""
    converter = AsyncBatchYamlConverter()
    yaml_list = [
        "- name: Alice\n  age: 30",
        "- name: Bob\n  age: 25"
    ]
    
    results = await converter.to_csv(yaml_list)
    
    assert len(results) == 2


@pytest.mark.asyncio
async def test_async_batch_yaml_from_csv():
    """Test async batch CSV to YAML conversion."""
    converter = AsyncBatchYamlConverter()
    csv_list = [
        "name,age\nAlice,30",
        "name,age\nBob,25"
    ]
    
    results = await converter.from_csv(csv_list)
    
    assert len(results) == 2


@pytest.mark.asyncio
async def test_async_batch_yaml_validate():
    """Test async batch YAML validation."""
    yaml_list = [
        "valid: yaml",
        "another: valid",
        ": invalid"
    ]
    
    results = await AsyncBatchYamlConverter.validate(yaml_list)
    
    assert len(results) == 3
    assert results[0]['is_valid'] is True
    assert results[1]['is_valid'] is True
    assert results[2]['is_valid'] is False


@pytest.mark.asyncio
async def test_async_batch_yaml_with_encryption():
    """Test async batch YAML conversion with encryption."""
    key = Fernet.generate_key()
    encryptor = Encryptor(key)
    converter = AsyncBatchYamlConverter(encryptor)
    
    yaml_list = ["name: Alice", "name: Bob"]
    encrypted_inputs = [encryptor.encrypt(y) for y in yaml_list]
    
    results = await converter.to_toon(encrypted_inputs, conversion_mode="middleware")
    
    assert len(results) == 2
    for result in results:
        assert isinstance(result, str)


@pytest.mark.asyncio
async def test_async_batch_yaml_concurrency():
    """Test async batch YAML converter doesn't block event loop."""
    converter = AsyncBatchYamlConverter()
    
    async def heartbeat():
        beats = 0
        while beats < 5:
            await asyncio.sleep(0.1)
            beats += 1
        return beats
    
    data_list = [f"id: {i}" for i in range(50)]
    
    heartbeat_task = asyncio.create_task(heartbeat())
    conversion_task = asyncio.create_task(converter.to_toon(data_list))
    
    results, beats = await asyncio.gather(conversion_task, heartbeat_task)
    
    assert beats == 5
    assert len(results) == 50
