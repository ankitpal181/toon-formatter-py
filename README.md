# 🚀 TOON Converter (Python)

A lightweight library to convert between **TOON** (Token-Oriented Object Notation) and popular data formats (JSON, YAML, XML, CSV).

**Reduce your LLM token costs by up to 40%** using the TOON format!

## 📦 Installation

```bash
pip install toon-parse
```

## 🚀 Quick Start

### Basic Usage (Synchronous)

```python
from toon_parse import ToonConverter

# 1. Python Object to TOON
data = {"name": "Alice", "age": 30, "active": True}
toon_string = ToonConverter.from_json(data)
print(toon_string)
# Output:
# name: "Alice"
# age: 30
# active: true

# 2. TOON to Python Object
json_output = ToonConverter.to_json(toon_string)
print(json_output)
# Output: {'name': 'Alice', 'age': 30, 'active': True}
```

### Mixed Text Support (New!)

The library can now automatically extract and convert JSON, XML, and CSV data embedded within normal text. This is perfect for processing LLM outputs.

```python
from toon_parse import ToonConverter

# Text with embedded JSON
mixed_text = """
Here is the user profile you requested:
{
    "id": 101,
    "name": "Bob",
    "roles": ["admin", "editor"]
}
Please verify this information.
"""

# Automatically finds JSON, converts it to TOON, and preserves surrounding text
result = ToonConverter.from_json(mixed_text)
print(result)

# Output:
# Here is the user profile you requested:
# id: 101
# name: "Bob"
# roles[2]: "admin", "editor"
# Please verify this information.
```

## ⚡ Async Usage

For non-blocking operations in async applications (e.g., FastAPI, AIOHTTP), use `AsyncToonConverter`.

```python
import asyncio
from toon_parse import AsyncToonConverter

async def main():
    # Mixed text input
    text = 'Data: <user><name>Alice</name></user>'
    
    # Async conversion (XML -> TOON)
    toon_string = await AsyncToonConverter.from_xml(text)
    print(toon_string)
    # Output: Data: user:\n  name: "Alice"
    
    # Async parsing (TOON -> JSON String)
    # Set return_json=False to get a JSON dict instead of a string
    json_dict = await AsyncToonConverter.to_json(toon_string, return_json=False)
    print(json_dict)

asyncio.run(main())
```

## 📚 Features & Support

| Feature | JSON | XML | CSV | YAML | TOON |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Python Dict/List Input** | ✅ | N/A | N/A | N/A | N/A |
| **Pure String Input** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Mixed Text Support** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Async Support** | ✅ | ✅ | ✅ | ✅ | ✅ |

- **Mixed Text**: Supported for JSON, XML, and CSV. The converter will find *all* occurrences of the data format in the text and convert them to TOON, leaving surrounding text intact.
- **YAML & TOON**: Input must be a valid, complete string. Mixed text is not supported for these formats.

## 🛠 API Reference

### Core Converters

#### `ToonConverter` (Synchronous)
- `from_json(data)`: Converts dict, list, JSON string, or mixed text to TOON.
- `to_json(toon_string, return_json=False)`: Converts TOON to Python dict/list. Set `return_json=True`(default) to get a JSON string.
- `from_xml(xml_string)`: Converts XML string or mixed text to TOON.
- `from_csv(csv_string)`: Converts CSV string or mixed text to TOON.
- `from_yaml(yaml_string)`: Converts YAML string to TOON (no mixed text).
- `to_xml(toon_string)`: Converts TOON to XML.
- `to_csv(toon_string)`: Converts TOON to CSV.
- `to_yaml(toon_string)`: Converts TOON to YAML.
- `validate(toon_string)`: Validates TOON syntax. Returns `{'is_valid': bool, 'error': str}`.

#### `AsyncToonConverter` (Asynchronous)
- Mirrors all methods of `ToonConverter` but as `async` functions.
- Example: `await AsyncToonConverter.from_json(data)`

### Utility Functions

You can also import extraction functions directly if you need to extract data without converting it.

```python
from toon_parse import extract_json_from_string, extract_xml_from_string, extract_csv_from_string

text = "Some text {"key": "val"} more text"
json_str = extract_json_from_string(text)
# Returns: '{"key": "val"}'
```

## 📄 License

MIT License
