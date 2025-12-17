
import unittest
from toon_parse.utils import sanitize_tag_name, flatten_json, unflatten_object, extract_csv_from_string, extract_json_from_string

class TestEnhancedUtils(unittest.TestCase):
    
    def test_sanitize_tag_name(self):
        self.assertEqual(sanitize_tag_name("valid"), "valid")
        self.assertEqual(sanitize_tag_name("valid_123"), "valid_123")
        self.assertEqual(sanitize_tag_name("123invalid"), "_123invalid")
        self.assertEqual(sanitize_tag_name("inv@lid"), "inv_lid")
        self.assertEqual(sanitize_tag_name("foo bar"), "foo_bar")
        self.assertEqual(sanitize_tag_name(""), "_")
        self.assertEqual(sanitize_tag_name(None), "_")

    def test_flatten_json(self):
        data = {
            "user": {
                "name": "Alice",
                "address": {
                    "city": "Wonderland",
                    "zip": 12345
                }
            },
            "active": True
        }
        expected = {
            "user.name": "Alice",
            "user.address.city": "Wonderland",
            "user.address.zip": 12345,
            "active": True
        }
        self.assertEqual(flatten_json(data), expected)
        
        # Test List
        data_list = [{"a": 1, "b": {"c": 2}}, {"a": 3}]
        expected_list = [{"a": 1, "b.c": 2}, {"a": 3}]
        self.assertEqual(flatten_json(data_list), expected_list)

    def test_unflatten_object(self):
        data = {
            "user.name": "Alice",
            "user.address.city": "Wonderland",
            "user.address.zip": 12345,
            "active": True
        }
        expected = {
            "user": {
                "name": "Alice",
                "address": {
                    "city": "Wonderland",
                    "zip": 12345
                }
            },
            "active": True
        }
        self.assertEqual(unflatten_object(data), expected)
        
        # Test no dots
        data_simple = {"a": 1, "b": 2}
        self.assertEqual(unflatten_object(data_simple), data_simple)

    def test_extract_csv_robustness(self):
        # Mixed content where a JSON block might look like CSV lines if not careful
        mixed = """
Some text.
Here is a JSON block:
{
  "key": "value",
  "list": [1, 2, 3]
}
Here is a CSV block:
id,name
1,Alice
2,Bob
End.
"""
        extracted = extract_csv_from_string(mixed)
        expected = "id,name\n1,Alice\n2,Bob"
        self.assertEqual(extracted, expected)

    def test_extract_json_improved(self):
        # Case `key[2]` should not trigger JSON extraction if it's not a real array start
        text = "This is key[2] which is just text.\nHere is { \"real\": \"json\" }"
        extracted = extract_json_from_string(text)
        expected = '{ "real": "json" }'
        self.assertEqual(extracted, expected)

if __name__ == '__main__':
    unittest.main()
