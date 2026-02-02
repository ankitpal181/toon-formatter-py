import pytest
from toon_parse.csv_parse import BatchCsvConverter

def test_batch_csv_from_toon():
    """Verify BatchCsvConverter.from_toon with multiple items."""
    # Use block-style TOON to avoid validator inline issues
    toon_data = [
        '[2]{id,name}:\n  1,"Alice"\n  2,"Bob"',
        '[1]{id,name}:\n  3,"Charlie"'
    ]
    results = BatchCsvConverter.from_toon(toon_data)
    assert len(results) == 2
    assert 'id,name' in results[0]
    assert 'Alice' in results[0]
    assert 'Charlie' in results[1]

def test_batch_csv_to_toon():
    """Verify BatchCsvConverter.to_toon with multiple items."""
    csv_data = ['id,name\n1,Alice', 'id,name\n2,Bob']
    # Use block-style TOON for consistency
    results = BatchCsvConverter.to_toon(csv_data)
    assert len(results) == 2
    assert "id" in results[0]
    assert "1" in results[0]
    assert "Alice" in results[0]

def test_batch_csv_parallel():
    """Verify parallel execution in BatchCsvConverter."""
    csv_data = ['id,name\n1,Alice', 'id,name\n2,Bob', 'id,name\n3,Charlie']
    print(f"Input CSV data for parallel processing: {csv_data}")
    results = BatchCsvConverter.to_toon(csv_data, parallel=True)
    print(f"Results from parallel CSV processing: {results}")
    assert len(results) == 3
    assert any("id" in r and "1" in r for r in results)


def test_batch_csv_validate():
    """Verify BatchCsvConverter.validate."""
    csv_list = ['id,name\n1,Alice', 'id,name\n1"Alice'] # malformed csv?
    results = BatchCsvConverter.validate(csv_list)
    assert len(results) == 2
    assert results[0]['is_valid'] is True

def test_batch_csv_cross_format():
    """Verify cross-format methods in BatchCsvConverter."""
    json_data_list = ['[{"id": 1}]', '[{"id": 2}]']
    # to_json (CSV data to JSON list)
    csv_data = ['id\n1', 'id\n2']
    json_results = BatchCsvConverter.to_json(csv_data)
    assert len(json_results) == 2
    
    # from_json (JSON string to CSV string list)
    csv_results = BatchCsvConverter.from_json(json_data_list)
    assert len(csv_results) == 2
    assert 'id' in csv_results[0]
    assert '1' in csv_results[0]
