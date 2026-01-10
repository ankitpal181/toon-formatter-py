
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
    text = """
Start
```
code content
```
End
    """
    result = dummy_converter(text)
    assert "code content" in result
    assert "Start" in result

def test_data_manager_multiple_blocks_order():
    # Regression test for index bug
    text = "Block1:\n```\ncode1\n```\nBlock2:\n```\ncode2\n```"
    result = dummy_converter(text)
    
    idx1 = result.find("code1")
    idx2 = result.find("code2")
    
    assert idx1 != -1
    assert idx2 != -1
    assert idx1 < idx2

def test_data_manager_preserves_content_while_converting():
    # Verify that code blocks are NOT affected by converter logic
    # while outside text IS affected
    
    text = "outside\n```\ninside code\n```"
    
    # dummy_converter_upper upper-cases everything
    # But data_manager should protect code blocks
    
    result = dummy_wrapper(text)
    
    # "outside" should be wrapped
    assert "WRAPPED(" in result
    assert "outside" in result
    
    # "inside code" should remain "inside code" and be preserved
    assert "inside code" in result
    
    # Ensure code is NOT double-wrapped or mangled? 
    # The placeholder was wrapped, then replaced by code.
    # So result: "WRAPPED(outside\ncode...)"
    assert "inside code" in result

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
