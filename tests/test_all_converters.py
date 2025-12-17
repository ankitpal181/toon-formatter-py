
import unittest
import json
import yaml
import xml.etree.ElementTree as ET
from toon_parse import (
    ToonConverter, JsonConverter, YamlConverter, XmlConverter, CsvConverter
)

class TestAllConverters(unittest.TestCase):

    # --- JsonConverter Tests ---
    def test_json_converter(self):
        print("\nTesting JsonConverter...")
        data = {"name": "Alice", "age": 30}
        
        # To TOON
        toon = JsonConverter.to_toon(data)
        self.assertIn('name: "Alice"', toon)
        
        # From TOON (return_json=False to get dict)
        res = JsonConverter.from_toon(toon, return_json=False)
        self.assertEqual(res['name'], 'Alice')
        
        # To YAML
        yml = JsonConverter.to_yaml(data)
        self.assertIn('name: Alice', yml)
        
        # To XML
        xml = JsonConverter.to_xml(data)
        self.assertIn('<name>Alice</name>', xml)
        
        # To CSV (List)
        csv_data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        csv_out = JsonConverter.to_csv(csv_data)
        self.assertIn('id,name', csv_out)
        self.assertIn('1,Alice', csv_out)

        # Validate
        val = JsonConverter.validate(json.dumps(data))
        self.assertTrue(val['is_valid'])

    # --- YamlConverter Tests ---
    def test_yaml_converter(self):
        print("\nTesting YamlConverter...")
        yaml_str = "name: Alice\nage: 30"
        
        # To TOON
        toon = YamlConverter.to_toon(yaml_str)
        self.assertIn('name: "Alice"', toon)
        
        # To JSON (returns string by default)
        json_str = YamlConverter.to_json(yaml_str)
        jsonn = json.loads(json_str)
        self.assertEqual(jsonn['name'], 'Alice')
        
        # Validate
        val = YamlConverter.validate(yaml_str)
        self.assertTrue(val['is_valid'])

    # --- XmlConverter Tests ---
    def test_xml_converter(self):
        print("\nTesting XmlConverter...")
        xml_str = "<root><name>Alice</name><age>30</age></root>"
        
        # To TOON
        toon = XmlConverter.to_toon(xml_str)
        # XML to TOON often wraps in root
        self.assertIn('root', toon) 
        
        # To JSON
        jsonn_str = XmlConverter.to_json(xml_str)
        data = json.loads(jsonn_str)
        self.assertIn('root', data)
        self.assertEqual(data['root']['name'], 'Alice')

        # Validate
        val = XmlConverter.validate(xml_str)
        self.assertTrue(val['is_valid'])

    # --- CsvConverter Tests ---
    def test_csv_converter(self):
        print("\nTesting CsvConverter...")
        csv_str = "id,name\n1,Alice\n2,Bob"
        
        # To TOON
        toon = CsvConverter.to_toon(csv_str)
        # CSV to TOON produces tabular array
        # [2]{id,name}:
        #   1,"Alice"
        self.assertIn("1,", toon)
        self.assertIn('"Alice"', toon)
        
        # To JSON
        json_str = CsvConverter.to_json(csv_str)
        data = json.loads(json_str)
        self.assertEqual(data[0]['name'], 'Alice')
        
        # Validate
        val = CsvConverter.validate(csv_str)
        self.assertTrue(val['is_valid'])

    # --- NEW: Enhanced Features Tests ---
    
    def test_xml_sanitization_integration(self):
        print("\nTesting XML Sanitization Integration...")
        # JSON with invalid XML tag names
        data = {"123invalid": "data", "foo bar": "baz", "valid": "ok"}
        
        # Should convert without error, transforming keys
        xml_out = JsonConverter.to_xml(data)
        
        # Check sanitization results
        self.assertIn('<_123invalid>data</_123invalid>', xml_out)
        self.assertIn('<foo_bar>baz</foo_bar>', xml_out)
        self.assertIn('<valid>ok</valid>', xml_out)

    def test_csv_flattening_integration(self):
        print("\nTesting CSV Flattening Integration...")
        # Nested JSON to CSV
        data = [
            {"id": 1, "user": {"name": "Alice", "role": "admin"}},
            {"id": 2, "user": {"name": "Bob", "role": "user"}}
        ]
        
        csv_out = JsonConverter.to_csv(data)
        
        # Should have flattened headers
        self.assertIn('user.name', csv_out)
        self.assertIn('user.role', csv_out)
        self.assertIn('1,Alice,admin', csv_out) # Order depends on sort, but these should be present

    def test_csv_unflattening_integration(self):
        print("\nTesting CSV Unflattening Integration...")
        # CSV with dot-notation headers
        csv_str = "id,user.name,user.role\n1,Alice,admin"
        
        json_out = CsvConverter.to_json(csv_str)
        data = json.loads(json_out)
        
        # Should be unflattened back to objects
        # Note: _infer_type converts '1' to 1 (int)
        self.assertEqual(data[0]['id'], 1) 
        self.assertEqual(data[0]['user']['name'], 'Alice')
        self.assertEqual(data[0]['user']['role'], 'admin')

    def test_mixed_content_robustness(self):
        print("\nTesting Mixed Content Robustness...")
        # CSV with confusing JSON-like lines inside
        mixed_csv = """
Ignored header
id,name
1,Alice
{ "fake": "json" }
2,Bob
ignored footer
"""
        json_out_full = CsvConverter.to_json(mixed_csv)
        
        # Ensure extraction stopped before the fake json
        # Result should look like:
        # Ignored header
        # [{"id": 1, "name": "Alice"}]
        # { "fake": "json" }...
        
        self.assertIn('[{"id": 1, "name": "Alice"}]', json_out_full)
        # Ensure Bob is NOT in the JSON part
        self.assertNotIn('"Bob"', json_out_full)

    # --- Legacy ToonConverter Tests ---
    def test_toon_converter_sanitization(self):
        print("\nTesting Legacy ToonConverter Sanitization...")
        # Dictionary with invalid key -> TOON -> XML
        data = {"123invalid": "value"}
        toon = JsonConverter.to_toon(data) # Generate valid TOON
        
        # ToonConverter.to_xml should use build_tag which uses sanitize_tag_name
        xml = ToonConverter.to_xml(toon)
        self.assertIn('<_123invalid>value</_123invalid>', xml)

    def test_toon_converter_flattening(self):
        print("\nTesting Legacy ToonConverter Flattening...")
        # Nested data -> TOON -> CSV
        data = [{"user": {"name": "Alice"}}]
        toon = JsonConverter.to_toon(data)
        
        # ToonConverter.to_csv should use flatten_json
        csv_out = ToonConverter.to_csv(toon)
        self.assertIn('user.name', csv_out)
        self.assertIn('Alice', csv_out)

if __name__ == '__main__':
    unittest.main()
