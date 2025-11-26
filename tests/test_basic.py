import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from toon_parse import ToonConverter, json_to_toon, toon_to_json

class TestToonConverter(unittest.TestCase):
    def test_json_to_toon_primitive(self):
        self.assertEqual(json_to_toon(123), "123")
        self.assertEqual(json_to_toon("hello"), '"hello"')
        self.assertEqual(json_to_toon(True), "true")
        self.assertEqual(json_to_toon(None), "null")

    def test_json_to_toon_object(self):
        data = {"name": "Alice", "age": 30}
        expected = 'name: "Alice"\nage: 30'
        # Note: dict order is preserved in recent python, but let's be careful
        # My implementation iterates dict, so order depends on insertion (which is source order here).
        self.assertEqual(json_to_toon(data), expected)

    def test_json_to_toon_array(self):
        data = [1, 2, 3]
        expected = '  [3]: 1, 2, 3' # Wait, my implementation adds indentation?
        # json_to_toon(data, key='', depth=0)
        # indent = ''
        # Array of primitives:
        # return f"{indent}{key}[{length}]: {values}"
        # -> "[3]: 1, 2, 3"
        # Let's check my code.
        # indent = '  ' * depth -> ''
        # key = ''
        # return f"{indent}{key}[{length}]: {values}" -> "[3]: 1, 2, 3"
        self.assertEqual(json_to_toon(data), "[3]: 1, 2, 3")

    def test_toon_to_json_basic(self):
        toon = 'name: "Alice"\nage: 30'
        expected = {"name": "Alice", "age": 30}
        self.assertEqual(toon_to_json(toon), expected)

    def test_tabular_array(self):
        data = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
        # Expected:
        # [2]{id,name}:
        #   1,"Alice"
        #   2,"Bob"
        toon = json_to_toon(data)
        self.assertIn("[2]{id,name}:", toon)
        self.assertIn('  1,"Alice"', toon)
        
        # Round trip
        back = toon_to_json(toon)
        self.assertEqual(back, data)

if __name__ == '__main__':
    unittest.main()
