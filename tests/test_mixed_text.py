import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from toon_parse import (
    json_to_toon, toon_to_json,
    xml_to_toon, toon_to_xml,
    csv_to_toon, toon_to_csv,
    extract_json_from_string, extract_xml_from_string, extract_csv_from_string
)

class TestMixedTextSupport(unittest.TestCase):
    """Test mixed text support for JSON, XML, and CSV converters"""
    
    # ===== JSON Mixed Text Tests =====
    
    def test_json_string_input(self):
        """Test JSON string input (not mixed text, just pure JSON string)"""
        json_str = '{"name": "Alice", "age": 30}'
        result = json_to_toon(json_str)
        self.assertIn('name: "Alice"', result)
        self.assertIn('age: 30', result)
    
    def test_json_mixed_text_single_block(self):
        """Test JSON embedded in text"""
        text = 'Here is some data: {"name": "Bob", "score": 95} and more text'
        result = json_to_toon(text)
        self.assertIn('name: "Bob"', result)
        self.assertIn('score: 95', result)
        self.assertIn('Here is some data:', result)
        self.assertIn('and more text', result)
    
    def test_json_mixed_text_multiple_blocks(self):
        """Test multiple JSON blocks in text"""
        text = '''First: {"a": 1}
Second: {"b": 2}
Third: {"c": 3}'''
        result = json_to_toon(text)
        self.assertIn('a: 1', result)
        self.assertIn('b: 2', result)
        self.assertIn('c: 3', result)
    
    def test_json_object_input(self):
        """Test that dict/list objects still work"""
        data = {"key": "value"}
        result = json_to_toon(data)
        self.assertEqual(result, 'key: "value"')
    
    def test_json_array_string(self):
        """Test JSON array as string"""
        json_str = '[1, 2, 3]'
        result = json_to_toon(json_str)
        self.assertEqual(result, '[3]: 1, 2, 3')
    
    # ===== XML Mixed Text Tests =====
    
    def test_xml_string_input(self):
        """Test XML string input"""
        xml_str = '<person><name>Alice</name><age>30</age></person>'
        result = xml_to_toon(xml_str)
        self.assertIn('person:', result)
        self.assertIn('name: "Alice"', result)
        self.assertIn('age: "30"', result)
    
    def test_xml_mixed_text_single_block(self):
        """Test XML embedded in text"""
        text = 'Data: <user><id>1</id><name>Bob</name></user> end'
        result = xml_to_toon(text)
        self.assertIn('user:', result)
        self.assertIn('id: "1"', result)
        self.assertIn('name: "Bob"', result)
        self.assertIn('Data:', result)
        self.assertIn('end', result)
    
    def test_xml_mixed_text_multiple_blocks(self):
        """Test multiple XML blocks"""
        text = '''<a>1</a>
Some text
<b>2</b>'''
        result = xml_to_toon(text)
        self.assertIn('a: "1"', result)
        self.assertIn('b: "2"', result)
    
    # ===== CSV Mixed Text Tests =====
    
    def test_csv_string_input(self):
        """Test CSV string input"""
        csv_str = '''name,age
Alice,30
Bob,25'''
        result = csv_to_toon(csv_str)
        self.assertIn('[2]{name,age}:', result)
        self.assertIn('"Alice",30', result)
        self.assertIn('"Bob",25', result)
    
    def test_csv_mixed_text_single_block(self):
        """Test CSV embedded in text"""
        text = '''Here is data:
name,score
Alice,100
Bob,95
End of data'''
        result = csv_to_toon(text)
        self.assertIn('[2]{name,score}:', result)
        self.assertIn('"Alice",100', result)
        self.assertIn('Here is data:', result)
        self.assertIn('End of data', result)
    
    def test_csv_no_infinite_loop(self):
        """Test that CSV doesn't infinitely loop on TOON output"""
        csv_str = '''name,age
Alice,30'''
        result = csv_to_toon(csv_str)
        # Should contain valid TOON output ([1] because only 1 data row, header not counted)
        self.assertIn('[1]{name,age}:', result)
        # Should not have been double-converted (would have extra escaping or malformed structure)
        # Verify it's valid by converting back
        from toon_parse import toon_to_csv
        back = toon_to_csv(result)
        # Check that both columns and values are present (order may vary)
        self.assertIn('name', back)
        self.assertIn('age', back)
        self.assertIn('Alice', back)
        self.assertIn('30', back)
    
    # ===== Extraction Function Tests =====
    
    def test_extract_json_from_string(self):
        """Test JSON extraction"""
        text = 'prefix {"key": "value"} suffix'
        result = extract_json_from_string(text)
        self.assertEqual(result, '{"key": "value"}')
    
    def test_extract_json_array(self):
        """Test JSON array extraction"""
        text = 'data: [1, 2, 3] end'
        result = extract_json_from_string(text)
        self.assertEqual(result, '[1, 2, 3]')
    
    def test_extract_json_none_found(self):
        """Test extraction when no JSON present"""
        text = 'just plain text'
        result = extract_json_from_string(text)
        self.assertIsNone(result)
    
    def test_extract_xml_from_string(self):
        """Test XML extraction"""
        text = 'before <tag>content</tag> after'
        result = extract_xml_from_string(text)
        self.assertEqual(result, '<tag>content</tag>')
    
    def test_extract_xml_self_closing(self):
        """Test self-closing XML tag"""
        text = 'data <tag/> end'
        result = extract_xml_from_string(text)
        self.assertEqual(result, '<tag/>')
    
    def test_extract_xml_none_found(self):
        """Test extraction when no XML present"""
        text = 'just plain text'
        result = extract_xml_from_string(text)
        self.assertIsNone(result)
    
    def test_extract_csv_from_string(self):
        """Test CSV extraction"""
        text = '''Some text
a,b,c
1,2,3
4,5,6
More text'''
        result = extract_csv_from_string(text)
        self.assertIn('a,b,c', result)
        self.assertIn('1,2,3', result)
        self.assertIn('4,5,6', result)
        self.assertNotIn('Some text', result)
        self.assertNotIn('More text', result)
    
    def test_extract_csv_ignores_toon_arrays(self):
        """Test that CSV extraction ignores TOON array syntax"""
        toon_text = '''[2]{name,age}:
  "Alice",30
  "Bob",25'''
        result = extract_csv_from_string(toon_text)
        # Should return None because it starts with [N]
        self.assertIsNone(result)
    
    def test_extract_csv_none_found(self):
        """Test extraction when no CSV present"""
        text = 'just plain text without commas'
        result = extract_csv_from_string(text)
        self.assertIsNone(result)
    
    # ===== Edge Cases =====
    
    def test_json_empty_object(self):
        """Test empty object conversion"""
        result = json_to_toon({})
        self.assertEqual(result, '')
    
    def test_json_empty_array(self):
        """Test empty array conversion"""
        result = json_to_toon([])
        self.assertEqual(result, '[0]:')
    
    def test_json_nested_structure(self):
        """Test nested JSON structure"""
        data = {
            "user": {
                "name": "Alice",
                "contacts": ["email", "phone"]
            }
        }
        result = json_to_toon(data)
        self.assertIn('user:', result)
        self.assertIn('name: "Alice"', result)
        self.assertIn('contacts[2]:', result)
    
    def test_toon_to_json_with_return_json_true(self):
        """Test return_json parameter"""
        toon = 'name: "Alice"'
        result = toon_to_json(toon, return_json=True)
        self.assertIsInstance(result, str)
        self.assertIn('"name"', result)
        self.assertIn('"Alice"', result)
    
    def test_toon_to_json_with_return_json_false(self):
        """Test return_json=False returns dict"""
        toon = 'name: "Alice"'
        result = toon_to_json(toon, return_json=False)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {"name": "Alice"})

if __name__ == '__main__':
    unittest.main()
