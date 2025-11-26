import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from toon_parse import (
    yaml_to_toon, toon_to_yaml,
    xml_to_toon, toon_to_xml,
    csv_to_toon, toon_to_csv
)

class TestConverters(unittest.TestCase):
    
    # --- YAML Tests ---

    def test_yaml_to_toon_simple(self):
        yaml_str = """
name: Alice
age: 30
"""
        toon = yaml_to_toon(yaml_str)
        self.assertIn('name: "Alice"', toon)
        self.assertIn('age: 30', toon)

    def test_toon_to_yaml_simple(self):
        toon = 'name: "Alice"\nage: 30'
        yaml_str = toon_to_yaml(toon)
        self.assertIn('name: Alice', yaml_str)
        self.assertIn('age: 30', yaml_str)

    def test_yaml_to_toon_nested(self):
        yaml_str = """
user:
  name: Alice
  roles:
    - admin
    - editor
"""
        toon = yaml_to_toon(yaml_str)
        self.assertIn('user:', toon)
        self.assertIn('name: "Alice"', toon)
        self.assertIn('roles[2]:', toon)

    # --- XML Tests ---

    def test_xml_to_toon_simple(self):
        xml_str = "<user><name>Alice</name><age>30</age></user>"
        toon = xml_to_toon(xml_str)
        
        # Note: XML conversion wraps based on root element
        self.assertIn('user:', toon)
        self.assertIn('name: "Alice"', toon)
        # XML text content is usually string, but my converter might infer numbers?
        # JS version: assert.ok(toon.includes('age: "30"'));
        # My Python implementation of xml_to_json_object returns text.
        # Then json_to_toon formats it.
        # If text is "30", format_value("30") -> '"30"' (string).
        # Unless I added type inference in xml converter? 
        # I didn't add explicit type inference in xml_to_json_object, just .strip().
        # So it should be a string.
        self.assertIn('age: "30"', toon)

    def test_toon_to_xml_simple(self):
        toon = 'user:\n  name: "Alice"\n  age: 30'
        xml_str = toon_to_xml(toon)

        self.assertIn('<user>', xml_str)
        self.assertIn('<name>Alice</name>', xml_str)
        self.assertIn('<age>30</age>', xml_str)
        self.assertIn('</user>', xml_str)

    def test_xml_to_toon_attributes(self):
        xml_str = '<item id="123" type="widget">Content</item>'
        toon = xml_to_toon(xml_str)

        self.assertIn('item:', toon)
        self.assertIn('@attributes:', toon)
        self.assertIn('id: "123"', toon)
        self.assertIn('type: "widget"', toon)
        self.assertIn('#text: "Content"', toon)

    # --- CSV Tests ---

    def test_csv_to_toon_basic(self):
        csv_str = """name,age,active
Alice,30,true
Bob,25,false"""

        toon = csv_to_toon(csv_str)

        # Should detect as tabular array or array of objects
        self.assertIn('[2]{name,age,active}:', toon)
        self.assertIn('Alice', toon)
        self.assertIn('30', toon)
        self.assertIn('true', toon)

    def test_toon_to_csv_basic(self):
        toon = """
[2]{name,role}:
  "Alice","Admin"
  "Bob","User"
"""
        csv_str = toon_to_csv(toon)

        self.assertIn('name,role', csv_str)
        self.assertIn('Alice,Admin', csv_str)
        self.assertIn('Bob,User', csv_str)

    def test_csv_round_trip(self):
        original_csv = """name,score
Alice,100
Bob,95"""

        toon = csv_to_toon(original_csv)
        final_csv = toon_to_csv(toon)

        # Note: CSV module might change line endings or quoting, but content should be there
        self.assertIn('name', final_csv)
        self.assertIn('score', final_csv)
        self.assertIn('Alice', final_csv)
        self.assertIn('100', final_csv)

if __name__ == '__main__':
    unittest.main()
