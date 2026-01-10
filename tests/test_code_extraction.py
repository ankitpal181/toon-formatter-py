import pytest
from toon_parse.utils import extract_code_blocks

def test_markdown_extraction():
    text = """
Here is some code:
```python
def foo():
    return 1
```
End of code.
    """
    blocks = extract_code_blocks(text)
    assert len(blocks) == 1
    # Check structure
    assert isinstance(blocks[0], dict)
    assert 'code' in blocks[0]
    assert 'start' in blocks[0]
    assert 'end' in blocks[0]
    
    assert "def foo():" in blocks[0]['code']
    
    # Check slicing
    extracted_slice = text[blocks[0]['start']:blocks[0]['end']]
    assert extracted_slice.startswith("```python")
    assert extracted_slice.endswith("```")

def test_multiple_markdown_blocks():
    text = """
Block 1:
```
code1
```
Block 2:
```js
code2
```
    """
    blocks = extract_code_blocks(text)
    assert len(blocks) == 2
    assert blocks[0]['code'] == "code1"
    assert blocks[1]['code'] == "code2"
    
    # Validate indices are sequential
    assert blocks[0]['end'] < blocks[1]['start']

def test_naked_code_heuristic():
    text = """
This is normal text.

def naked_function():
    print("I am naked")
    return True

More normal text.
    """
    blocks = extract_code_blocks(text)
    assert len(blocks) == 1
    assert "def naked_function():" in blocks[0]['code']
    
    # Check slicing logic for heuristic (full paragraph)
    extracted_slice = text[blocks[0]['start']:blocks[0]['end']]
    assert "def naked_function():" in extracted_slice
    assert "More normal text" not in extracted_slice
    assert "This is normal text" not in extracted_slice

def test_naked_code_heuristic_precise_indices():
    # Setup text with known indices
    # 01234
    # Code\n\nNext
    text = "Code\n\nNext"
    # "Code" is code-like if we assume it passes is_code (which it won't, len < 5)
    # Let's use something that passes is_code. Note: is_code requires multiple lines.
    code = "import os\nprint(os.getcwd())"
    text = f"Intro\n\n{code}\n\nOutro"
    
    blocks = extract_code_blocks(text)
    assert len(blocks) == 1
    block = blocks[0]
    
    assert text[block['start']:block['end']] == code
    assert block['code'] == code

def test_mixed_ignores_naked_if_markdown_present():
    text = """
Here is a fence:
```
fenced
```

And here is naked code:

function naked() {
    return false;
}
    """
    blocks = extract_code_blocks(text)
    assert len(blocks) == 1
    assert blocks[0]['code'] == "fenced"

def test_no_code():
    text = "Just some plain text.\nWith multiple lines."
    assert extract_code_blocks(text) == []

def test_empty_input():
    assert extract_code_blocks("") == []
    assert extract_code_blocks(None) == []
