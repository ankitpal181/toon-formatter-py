import pytest
import os
import tempfile
from toon_parse.batch_converter import BatchToonConverter

@pytest.fixture
def batch_converter():
    return BatchToonConverter()

def test_from_json_list(batch_converter):
    """Verify conversion of a list of JSON objects to TOON strings."""
    data = [{"key": "value"}, {"key2": "value2"}]
    result = batch_converter.from_json(data)
    assert isinstance(result, list)
    assert len(result) == 2
    assert 'key: "value"' in result[0]
    assert 'key2: "value2"' in result[1]

def test_to_json_list(batch_converter):
    """Verify conversion of a list of TOON strings to JSON objects."""
    toon_data = ['key: "value"', 'key2: "value2"']
    result = batch_converter.to_json(toon_data, return_json=False)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == {"key": "value"}
    assert result[1] == {"key2": "value2"}

def test_validate_static():
    """Verify static validation call."""
    toon_data = ['key: "value"', 'invalid_toon:'] 
    # 'invalid_toon:' might be valid depending on parser laxness, 
    # but let's assume standard k:v. 
    # Actually 'invalid_toon:' is valid key with empty value (null/dict).
    
    # Let's use something definitely invalid if possible, or just check structure.
    # The validator returns a list of result dicts.
    results = BatchToonConverter.validate(toon_data)
    assert isinstance(results, list)
    assert len(results) == 2
    assert results[0]['is_valid'] is True

def test_validate_instance(batch_converter):
    """Verify instance validation call."""
    toon_data = ['key: "value"']
    results = batch_converter.validate(toon_data)
    assert isinstance(results, list)
    assert results[0]['is_valid'] is True

def test_file_processing(batch_converter):
    """Verify processing from a file path."""
    content = '{"key": "file_value"}'
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # Test from_json with file path
        # from_json expects list or file path. 
        # CAUTION: from_json usually expects JSON *object* or string.
        # batch_modulator reads file content as string.
        # json_to_toon handles string input by extracting JSON blocks.
        
        result = batch_converter.from_json(tmp_path)
        # Result should be a single string (converted content of file)
        assert isinstance(result, str)
        assert 'key: "file_value"' in result
        
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def test_validate_file_processing():
    """Verify validate with a file path."""
    content = 'key: "file_value"'
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
        
    try:
        # validate static with file path
        result = BatchToonConverter.validate(tmp_path)
        # Should return a single dict result for the file content
        assert isinstance(result, dict) 
        assert result['is_valid'] is True
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
