import pytest
from toon_parse.yaml_parse import BatchYamlConverter

def test_batch_yaml_from_toon():
    """Verify BatchYamlConverter.from_toon with multiple items."""
    toon_data = ['id: 1', 'id: 2']
    results = BatchYamlConverter.from_toon(toon_data)
    assert len(results) == 2
    assert 'id: 1' in results[0]
    assert 'id: 2' in results[1]

def test_batch_yaml_to_toon():
    """Verify BatchYamlConverter.to_toon with multiple items."""
    yaml_data = ['id: 1', 'id: 2']
    results = BatchYamlConverter.to_toon(yaml_data)
    assert len(results) == 2
    assert "id: 1" in results[0]
    assert "id: 2" in results[1]

def test_batch_yaml_parallel():
    """Verify parallel execution in BatchYamlConverter."""
    yaml_data = ['id: 1', 'id: 2', 'id: 3']
    results = BatchYamlConverter.to_toon(yaml_data, parallel=True)
    assert len(results) == 3
    assert any("id: 1" in r for r in results)

def test_batch_yaml_validate():
    """Verify BatchYamlConverter.validate."""
    yaml_list = ['id: 1', 'id: 2']
    results = BatchYamlConverter.validate(yaml_list)
    assert len(results) == 2
    assert all(r['is_valid'] for r in results)

def test_batch_yaml_cross_format():
    """Verify cross-format methods in BatchYamlConverter."""
    json_data_list = ['{"id": 1}', '{"id": 2}']
    # to_json (YAML data to JSON list)
    yaml_data = ['id: 1', 'id: 2']
    json_results = BatchYamlConverter.to_json(yaml_data, return_json=False)
    assert len(json_results) == 2
    assert json_results[0]['id'] == 1
    
    # from_json (JSON string to YAML string list)
    yaml_results = BatchYamlConverter.from_json(json_data_list)
    assert len(yaml_results) == 2
    assert 'id: 1' in yaml_results[0]
