import pytest
import time
from toon_parse.batch_converter import BatchToonConverter

@pytest.fixture
def batch_converter():
    return BatchToonConverter()

def test_parallel_static_call():
    """Verify parallel execution with static call."""
    data = ['{"id": 1}', '{"id": 2}', '{"id": 3}']
    # Using parallel=True
    # Since we can't easily mock the threading behavior to prove it ran in parallel without
    # injecting delays, we mostly verify that it returns correct results without crashing.
    results = BatchToonConverter.from_json(data, parallel=True)
    assert isinstance(results, list)
    assert len(results) == 3
    # Order is not guaranteed in parallel execution usually, but ThreadPoolExecutor.map preserves it.
    # However, user implementation uses as_completed, so order is NOT guaranteed.
    # We should check existence of all items.
    assert any('id: 1' in r for r in results)
    assert any('id: 2' in r for r in results)
    assert any('id: 3' in r for r in results)

def test_parallel_instance_call(batch_converter):
    """Verify parallel execution with instance call."""
    data = ['{"id": 1}', '{"id": 2}']
    results = batch_converter.from_json(data, parallel=True)
    assert len(results) == 2
    assert any('id: 1' in r for r in results)
    assert any('id: 2' in r for r in results)

def test_parallel_validate():
    """Verify parallel validation."""
    data = ['key: "val"', 'BROKEN_TOON'] 
    # Valid and invalid mixed
    results = BatchToonConverter.validate(data, parallel=True)
    assert len(results) == 2
    
    # Check that we have one valid and one invalid result (order unknown)
    valid_count = sum(1 for r in results if r['is_valid'])
    invalid_count = sum(1 for r in results if not r['is_valid'])
    
    assert valid_count == 1
    assert invalid_count == 1

def test_series_execution_regression(batch_converter):
    """Verify series execution (parallel=False) still works."""
    data = ['{"id": 1}', '{"id": 2}']
    # Explicit parallel=False
    results = batch_converter.from_json(data, parallel=False)
    assert len(results) == 2
    # Series execution usually preserves order (list comprehension)
    assert 'id: 1' in results[0]
    assert 'id: 2' in results[1]
    
    # Implicit parallel=False (default)
    results_default = batch_converter.from_json(data)
    assert len(results_default) == 2
    assert 'id: 1' in results_default[0]

