import pytest
from toon_parse.utils import extract_code_blocks

def test_heuristic_extraction():
    text = """
Here is some code:

def foo():
    return 1

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
    
    # Check slicing (Note: includes the newline and spaces if any, depending on current_pos)
    extracted_slice = text[blocks[0]['start']:blocks[0]['end']]
    assert "def foo():" in extracted_slice

def test_multiple_heuristic_blocks():
    text = """
Block 1:

import os
print(os.getcwd())

Block 2:

function test() {
    return true;
}
    """
    blocks = extract_code_blocks(text)
    assert len(blocks) == 2
    assert "import os" in blocks[0]['code']
    assert "function test()" in blocks[1]['code']
    
    # Validate indices are sequential
    assert blocks[0]['end'] < blocks[1]['start']

def test_precise_indices():
    # Setup text with known indices
    code = "import os\nprint(os.getcwd())"
    text = f"Intro\n\n{code}\n\nOutro"
    
    blocks = extract_code_blocks(text)
    assert len(blocks) == 1
    block = blocks[0]
    
    # Slicing should return the code part exactly as it was between \n\n
    assert text[block['start']:block['end']] == code
    assert block['code'] == code

def test_no_code():
    text = "Just some plain text.\nWith multiple lines."
    assert extract_code_blocks(text) == []

def test_empty_input():
    assert extract_code_blocks("") == []
    assert extract_code_blocks(None) == []
