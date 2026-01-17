
import pytest
from toon_parse.utils import data_manager

@data_manager
def dummy_converter(text):
    return text

@data_manager
def dummy_wrapper(text):
    return f"WRAPPED({text})"

def test_data_manager_no_code():
    text = "Just plain text"
    assert dummy_converter(text) == text

def test_data_manager_single_block():
    # Heuristic based block
    text = """
Start

def foo():
    return 1

End
    """
    result = dummy_converter(text)
    assert "def foo():" in result
    assert "Start" in result

def test_data_manager_multiple_blocks_order():
    # Regression test for index bug
    text = "Block1:\n\nimport os\n\nBlock2:\n\nclass MyClass:\n    pass"
    result = dummy_converter(text)
    
    idx1 = result.find("import os")
    idx2 = result.find("class MyClass:")
    
    assert idx1 != -1
    assert idx2 != -1
    assert idx1 < idx2

def test_data_manager_preserves_content_while_converting():
    # Verify that code blocks are NOT affected by converter logic
    # while outside text IS affected
    
    text = "outside\n\ndef my_code():\n    pass"
    
    result = dummy_wrapper(text)
    
    # "outside" should be wrapped
    assert "WRAPPED(" in result
    assert "outside" in result
    
    # "my_code" should remain "my_code" and be preserved
    assert "def my_code():" in result
    
    # Ensure code is NOT mangled
    assert "def my_code():" in result

def test_data_manager_naked_code():
    # Test with heuristic-based naked code blocks
    text = """
Here is a function:

def foo():
    return True

End.
    """
    result = dummy_wrapper(text)
    
    assert "WRAPPED(" in result
    assert "Here is a function" in result
    # Function def should be preserved
    assert "def foo():" in result

def test_data_manager_pass_through_dict():
    # Test that dict inputs are passed through without error
    data = {"key": "value"}
    result = dummy_converter(data)
    assert result == data
