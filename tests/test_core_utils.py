import pytest
from toon_parse.utils import (
    parse_value, format_value, split_by_delimiter, 
    extract_json_from_string, extract_xml_from_string, extract_csv_from_string
)

def test_parse_value():
    assert parse_value("true") is True
    assert parse_value("false") is False
    assert parse_value("null") is None
    assert parse_value("123") == 123
    assert parse_value("12.34") == 12.34
    assert parse_value('"string"') == "string"
    assert parse_value('"str with \\"quote\\""') == 'str with "quote"'
    # Edge cases
    assert parse_value("0123") == "0123" # Leading zero string
    assert parse_value("0") == 0

def test_format_value():
    assert format_value(True) == "true"
    assert format_value(False) == "false"
    assert format_value(None) == "null"
    assert format_value(123) == "123"
    assert format_value("simple") == '"simple"'
    assert format_value('quo"te') == '"quo\\"te"'

def test_split_by_delimiter():
    assert split_by_delimiter("a,b,c", ",") == ["a", "b", "c"]
    assert split_by_delimiter('a,"b,c",d', ",") == ["a", '"b,c"', "d"]
    assert split_by_delimiter('a|b|c', "|") == ["a", "b", "c"]

def test_extract_json_mixed():
    text = 'Pre text {"key": "val"} Post text'
    assert extract_json_from_string(text) == '{"key": "val"}'
    
    text_array = 'Start [1, 2, 3] End'
    assert extract_json_from_string(text_array) == '[1, 2, 3]'
    
    # Test nesting
    text_nested = 'Mixed {"a": {"b": 1}} content'
    assert extract_json_from_string(text_nested) == '{"a": {"b": 1}}'

def test_extract_xml_mixed():
    text = 'Pre <root><item>1</item></root> Post'
    assert extract_xml_from_string(text) == '<root><item>1</item></root>'
    
    text_self_closing = 'Pre <item id="1" /> Post'
    assert extract_xml_from_string(text_self_closing) == '<item id="1" />'

def test_extract_csv_mixed():
    # CSV extraction is heuristic-based
    text = "Header text\nid,name,age\n1,Alice,30\n2,Bob,25\nFooter text"
    expected = "id,name,age\n1,Alice,30\n2,Bob,25"
    assert extract_csv_from_string(text).strip() == expected
