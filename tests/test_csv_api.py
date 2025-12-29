import pytest
from toon_parse import CsvConverter, AsyncCsvConverter

@pytest.fixture
def converter():
    return CsvConverter()

@pytest.fixture
def async_converter():
    return AsyncCsvConverter()

def test_csv_to_json(converter):
    csv = "id,name\n1,Alice"
    res = converter.to_json(csv)
    if isinstance(res, str):
        import json
        res = json.loads(res)
    assert len(res) == 1
    assert res[0]['id'] == 1
    assert res[0]['name'] == 'Alice'

def test_json_to_csv(converter):
    data = [{"id": 1, "name": "Alice"}]
    csv = converter.from_json(data)
    assert 'id,name' in csv
    assert '1,Alice' in csv

def test_csv_flattening(converter):
    # Nested object to CSV
    data = [{"user": {"id": 1, "name": "Alice"}}]
    csv = converter.from_json(data)
    # Should flatten to user.id, user.name
    assert 'user.id' in csv
    assert 'user.name' in csv

def test_csv_unflattening(converter):
    csv = "user.id,user.name\n1,Alice"
    res = converter.to_json(csv)
    if isinstance(res, str):
        import json
        res = json.loads(res)
    assert res[0]['user']['id'] == 1
    assert res[0]['user']['name'] == 'Alice'

@pytest.mark.asyncio
async def test_to_json_async(async_converter):
    csv = "col1,col2\nval1,val2"
    res = await async_converter.to_json(csv)
    if isinstance(res, str):
        import json
        res = json.loads(res)
    assert res[0]['col1'] == 'val1'
