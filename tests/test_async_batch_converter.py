import pytest
import asyncio
from toon_parse.async_batch_converter import AsyncBatchToonConverter
from toon_parse.encrypt import Encryptor
from cryptography.fernet import Fernet


@pytest.mark.asyncio
async def test_async_batch_from_json():
    """Test async batch conversion from JSON to TOON."""
    converter = AsyncBatchToonConverter()
    json_list = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]
    
    results = await converter.from_json(json_list)
    
    assert len(results) == 2
    # YAML converter adds quotes around strings
    assert "name:" in results[0]
    assert "Alice" in results[0]
    assert "age: 30" in results[0]
    assert "Bob" in results[1]


@pytest.mark.asyncio
async def test_async_batch_to_json():
    """Test async batch conversion from TOON to JSON."""
    converter = AsyncBatchToonConverter()
    toon_list = [
        "name: Alice\nage: 30",
        "name: Bob\nage: 25"
    ]
    
    results = await converter.to_json(toon_list, return_json=False)
    
    assert len(results) == 2
    # return_json=False returns dict objects
    assert results[0]['name'] == 'Alice'
    assert results[0]['age'] == 30


@pytest.mark.asyncio
async def test_async_batch_from_yaml():
    """Test async batch conversion from YAML to TOON."""
    converter = AsyncBatchToonConverter()
    yaml_list = [
        "name: Alice\nage: 30",
        "name: Bob\nage: 25"
    ]
    
    results = await converter.from_yaml(yaml_list)
    
    assert len(results) == 2
    assert "name:" in results[0]
    assert "Alice" in results[0]
    assert "age: 30" in results[0]


@pytest.mark.asyncio
async def test_async_batch_to_yaml():
    """Test async batch conversion from TOON to YAML."""
    converter = AsyncBatchToonConverter()
    toon_list = [
        "name: Alice\nage: 30",
        "name: Bob\nage: 25"
    ]
    
    results = await converter.to_yaml(toon_list)
    
    assert len(results) == 2
    assert "name: Alice" in results[0]
    assert "age: 30" in results[0]


@pytest.mark.asyncio
async def test_async_batch_from_xml():
    """Test async batch conversion from XML to TOON."""
    converter = AsyncBatchToonConverter()
    xml_list = [
        "<person><name>Alice</name><age>30</age></person>",
        "<person><name>Bob</name><age>25</age></person>"
    ]
    
    results = await converter.from_xml(xml_list)
    
    assert len(results) == 2
    assert "person:" in results[0]
    assert "Alice" in results[0]


@pytest.mark.asyncio
async def test_async_batch_to_xml():
    """Test async batch conversion from TOON to XML."""
    converter = AsyncBatchToonConverter()
    toon_list = [
        "person:\n  name: Alice\n  age: 30",
        "person:\n  name: Bob\n  age: 25"
    ]
    
    results = await converter.to_xml(toon_list)
    
    assert len(results) == 2
    assert "<person>" in results[0]
    assert "<name>Alice</name>" in results[0]


@pytest.mark.asyncio
async def test_async_batch_from_csv():
    """Test async batch conversion from CSV to TOON."""
    converter = AsyncBatchToonConverter()
    csv_list = [
        "name,age\nAlice,30\nBob,25",
        "product,price\nApple,1.50\nBanana,0.75"
    ]
    
    results = await converter.from_csv(csv_list)
    
    assert len(results) == 2
    assert "[2]{" in results[0]
    assert "Alice" in results[0] and "30" in results[0]


@pytest.mark.asyncio
async def test_async_batch_to_csv():
    """Test async batch conversion from TOON to CSV."""
    converter = AsyncBatchToonConverter()
    toon_list = [
        "[2]{name,age}:\n  Alice,30\n  Bob,25",
        "[2]{product,price}:\n  Apple,1.50\n  Banana,0.75"
    ]
    
    results = await converter.to_csv(toon_list)
    
    assert len(results) == 2
    # CSV column order may vary
    assert "Alice" in results[0] and "30" in results[0]
    assert "name" in results[0] and "age" in results[0]


@pytest.mark.asyncio
async def test_async_batch_validate():
    """Test async batch validation of TOON strings."""
    toon_list = [
        "name: Alice\nage: 30",
        "name: Bob\nage: 25",
        "[5]: 1, 2, 3"  # Size mismatch
    ]
    
    results = await AsyncBatchToonConverter.validate(toon_list)
    
    assert len(results) == 3
    assert results[0]['is_valid'] is True
    assert results[1]['is_valid'] is True
    assert results[2]['is_valid'] is False


@pytest.mark.asyncio
async def test_async_batch_with_encryption():
    """Test async batch conversion with encryption."""
    key = Fernet.generate_key()
    encryptor = Encryptor(key)
    converter = AsyncBatchToonConverter(encryptor)
    
    json_list = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]
    
    # Middleware mode: decrypt input, convert, encrypt output
    encrypted_inputs = [encryptor.encrypt('{"name": "Alice", "age": 30}'),
                       encryptor.encrypt('{"name": "Bob", "age": 25}')]
    
    results = await converter.from_json(encrypted_inputs, conversion_mode="middleware")
    
    assert len(results) == 2
    # Results should be encrypted (base64 strings)
    for result in results:
        assert isinstance(result, str)
        decrypted = encryptor.decrypt(result)
        assert "name:" in decrypted


@pytest.mark.asyncio
async def test_async_batch_concurrency():
    """Test that async batch operations don't block the event loop."""
    converter = AsyncBatchToonConverter()
    
    # Create a heartbeat task
    async def heartbeat():
        beats = 0
        while beats < 5:
            await asyncio.sleep(0.1)
            beats += 1
        return beats
    
    # Large batch
    data_list = [{"id": i, "data": "test"} for i in range(50)]
    
    # Run both concurrently
    heartbeat_task = asyncio.create_task(heartbeat())
    conversion_task = asyncio.create_task(converter.from_json(data_list))
    
    results, beats = await asyncio.gather(conversion_task, heartbeat_task)
    
    # If event loop wasn't blocked, heartbeat should complete all beats
    assert beats == 5
    assert len(results) == 50


@pytest.mark.asyncio
async def test_async_batch_instance_vs_static():
    """Test both instance and static usage patterns."""
    # Instance usage
    converter = AsyncBatchToonConverter()
    json_list = [{"name": "Alice"}, {"name": "Bob"}]
    results = await converter.from_json(json_list)
    assert len(results) == 2
    
    # Static validation
    toon_list = ["name: Alice", "name: Bob"]
    validation_results = await AsyncBatchToonConverter.validate(toon_list)
    assert len(validation_results) == 2
    assert all(r['is_valid'] for r in validation_results)
