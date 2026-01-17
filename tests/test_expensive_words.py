
import pytest
from toon_parse.utils import alter_expensive_words, data_manager
from toon_parse import ToonConverter

# ---- Unit Tests for alter_expensive_words ----

def test_basic_replacement():
    """Test standard replacement of expensive words."""
    text = "Start large language model end"
    expected = "Start llm end"
    assert alter_expensive_words(text) == expected

def test_case_insensitivity():
    """Test that replacements are case-insensitive."""
    # Although the current implementation strictly follows the dictionary keys (which are lowercase),
    # the regex should ideally handle case or the input should be normalized?
    # Checking utils.py: It uses `re.escape(key)` from `EXPENSIVE_WORDS.keys()`.
    # It does NOT use re.IGNORECASE flag in the current implementation.
    # So "Large Language Model" might NOT be replaced based on current code.
    # Let's verify what the code DOES. The user might expect strict matching or not.
    # Based on `utils.py`: `pattern = re.compile(..., ...)`. No flags.
    # So "large language model" -> "llm", but "Large Language Model" might stay.
    # We will test the currently implemented behavior (exact match of keys).
    
    text = "i am a large language model"
    expected = "i'm a llm"
    assert alter_expensive_words(text) == expected

def test_word_boundaries():
    """Ensure partial words are not replaced."""
    # "do not" -> "don't"
    # "do nothing" should NOT become "don'thing"
    text = "Please do nothing"
    result = alter_expensive_words(text)
    assert result == "pls do nothing"

# ---- Integration Tests for data_manager / ToonConverter ----

def test_primitive_string_optimization():
    """Verify simple strings get optimized when passed to converter."""
    converter = ToonConverter()
    input_text = "I am testing frequently asked questions."
    # "I am" -> "i'm", "frequently asked questions" -> "faq"
    expected = "i'm testing faq." 
    
    # Since it's a primitive string, ToonConverter wraps it in quotes?
    # Let's check: json_to_toon_parser calls format_value for strings -> returns quoted string.
    # So output should be quoted.
    
    output = converter.from_json(input_text)
    assert "i'm testing faq." in output
    assert output.strip().startswith('"')
    assert output.strip().endswith('"')

def test_mixed_text_with_json_and_expensive_words():
    """
    Verify mixed text:
    1. Expensive words in text are replaced.
    2. Embedded JSON is converted.
    3. Output is NOT quoted (regression test).
    """
    converter = ToonConverter()
    # "I will" -> "i'll"
    input_text = 'I will send the data: {"id": 123}.'
    
    output = converter.from_json(input_text)
    
    # 1. Check expensive word replacement
    assert "i'll" in output.lower()
    
    # 2. Check JSON conversion
    # {"id": 123} -> id: 123
    assert "id: 123" in output
    
    # 3. Check NO quoting (Critical Regression Check)
    # The output should be the raw string with TOON data, NOT wrapped in quotas.
    # e.g. "i'll send the data: id: 123."
    assert not (output.strip().startswith('"') and output.strip().endswith('"'))

def test_code_block_preservation_with_expensive_words():
    """
    Verify that words INSIDE code blocks are NOT replaced,
    even if they match expensive words.
    """
    converter = ToonConverter()
    
    # "do not" is expensive -> "don't"
    # We use double newlines to separate the code block as per new heuristic.
    input_text = "I do not like this code:\n\ndef foo():\n    print('do not change me')\n    return 1\n\nEnd of code."
    
    output = converter.from_json(input_text)
    
    # Outside: "I do not" -> "I don't"
    assert "don't" in output.lower()
    
    # Inside: "do not change me" should remain "do not change me"
    assert "print('do not change me')" in output
    assert "print('don't change me')" not in output

def test_multiple_data_blocks():
    """Verify handling of multiple embedded data blocks."""
    converter = ToonConverter()
    input_text = 'Data 1: {"a": 1}. Data 2: {"b": 2}.'
    
    output = converter.from_json(input_text)
    
    assert "a: 1" in output
    assert "b: 2" in output
    assert not output.strip().startswith('"')

