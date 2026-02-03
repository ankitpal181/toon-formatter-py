import pytest
import asyncio
from toon_parse.json_parse import AsyncBatchJsonConverter
from toon_parse.encrypt import Encryptor
from cryptography.fernet import Fernet


@pytest.mark.asyncio
async def test_async_batch_json_to_toon():
    """Test async batch conversion from JSON to TOON."""
    converter = AsyncBatchJsonConverter()
    json_list = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]
    
    results = await converter.to_toon(json_list)
    
    assert len(results) == 2
    assert "name:" in results[0]
    assert "Alice" in results[0]


@pytest.mark.asyncio
async def test_async_batch_json_from_toon():
    """Test async batch conversion from TOON to JSON."""
    converter = AsyncBatchJsonConverter()
    toon_list = [
        "name: Alice\nage: 30",
        "name: Bob\nage: 25"
    ]
    
    results = await converter.from_toon(toon_list, return_json=False)
    
    assert len(results) == 2
    assert results[0]['name'] == 'Alice'
    assert results[0]['age'] == 30


@pytest.mark.asyncio
async def test_async_batch_json_to_yaml():
    """Test async batch JSON to YAML conversion."""
    converter = AsyncBatchJsonConverter()
    json_list = [{"city": "NYC"}, {"city": "LA"}]
    
    results = await converter.to_yaml(json_list)
    
    assert len(results) == 2
    assert "city:" in results[0]
    assert "NYC" in results[0]


@pytest.mark.asyncio
async def test_async_batch_json_from_yaml():
    """Test async batch YAML to JSON conversion."""
    converter = AsyncBatchJsonConverter()
    yaml_list = ["city: NYC", "city: LA"]
    
    results = await converter.from_yaml(yaml_list, return_json=False)
    
    assert len(results) == 2
    assert results[0]['city'] == 'NYC'


@pytest.mark.asyncio
async def test_async_batch_json_to_xml():
    """Test async batch JSON to XML conversion."""
    converter = AsyncBatchJsonConverter()
    json_list = [{"user": {"name": "Alice"}}, {"user": {"name": "Bob"}}]
    
    results = await converter.to_xml(json_list)
    
    assert len(results) == 2
    assert "<user>" in results[0]
    assert "Alice" in results[0]


@pytest.mark.asyncio
async def test_async_batch_json_from_xml():
    """Test async batch XML to JSON conversion."""
    converter = AsyncBatchJsonConverter()
    xml_list = ["<user><name>Alice</name></user>", "<user><name>Bob</name></user>"]
    
    results = await converter.from_xml(xml_list)
    
    assert len(results) == 2
    # Results are strings in batch mode
    assert isinstance(results[0], str)
    assert "Alice" in results[0]


@pytest.mark.asyncio
async def test_async_batch_json_to_csv():
    """Test async batch JSON to CSV conversion."""
    converter = AsyncBatchJsonConverter()
    json_list = [
        [{"name": "Alice", "age": 30}],
        [{"name": "Bob", "age": 25}]
    ]
    
    results = await converter.to_csv(json_list)
    
    assert len(results) == 2
    assert "Alice" in results[0]


@pytest.mark.asyncio
async def test_async_batch_json_from_csv():
    """Test async batch CSV to JSON conversion."""
    converter = AsyncBatchJsonConverter()
    csv_list = [
        "name,age\nAlice,30",
        "name,age\nBob,25"
    ]
    
    results = await converter.from_csv(csv_list)
    
    assert len(results) == 2
    # Results are strings in batch mode
    assert isinstance(results[0], str)
    assert "Alice" in results[0]


@pytest.mark.asyncio
async def test_async_batch_json_validate():
    """Test async batch JSON validation."""
    json_list = [
        '{"valid": "json"}',
        '{"another": "valid"}',
        'invalid json'
    ]
    
    results = await AsyncBatchJsonConverter.validate(json_list)
    
    assert len(results) == 3
    assert results[0]['is_valid'] is True
    assert results[1]['is_valid'] is True
    assert results[2]['is_valid'] is False


@pytest.mark.asyncio
async def test_async_batch_json_with_encryption():
    """Test async batch JSON conversion with encryption."""
    key = Fernet.generate_key()
    encryptor = Encryptor(key)
    converter = AsyncBatchJsonConverter(encryptor)
    
    json_list = ['{"name": "Alice"}', '{"name": "Bob"}']
    encrypted_inputs = [encryptor.encrypt(j) for j in json_list]
    
    results = await converter.to_toon(encrypted_inputs, conversion_mode="middleware")
    
    assert len(results) == 2
    for result in results:
        assert isinstance(result, str)


@pytest.mark.asyncio
async def test_async_batch_json_concurrency():
    """Test async batch JSON converter doesn't block event loop."""
    converter = AsyncBatchJsonConverter()
    
    async def heartbeat():
        beats = 0
        while beats < 5:
            await asyncio.sleep(0.1)
            beats += 1
        return beats
    
    data_list = [{"id": i} for i in range(50)]
    
    heartbeat_task = asyncio.create_task(heartbeat())
    conversion_task = asyncio.create_task(converter.to_toon(data_list))
    
    results, beats = await asyncio.gather(conversion_task, heartbeat_task)
    
    assert beats == 5
    assert len(results) == 50
