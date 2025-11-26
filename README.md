# 🚀 TOON Converter (Python)

A lightweight library to convert between **TOON** (Token-Oriented Object Notation) and popular data formats (JSON, YAML, XML, CSV).

**Reduce your LLM token costs by up to 40%** using the TOON format!

## 📦 Installation

```bash
pip install toon-parse
```

## 🚀 Quick Start

```python
from toon_parse import ToonConverter

# JSON to TOON
data = {"name": "Alice", "age": 30, "active": True}
toon_string = ToonConverter.from_json(data)
print(toon_string)
# Output:
# name: "Alice"
# age: 30
# active: true

# TOON to JSON
json_output = ToonConverter.to_json(toon_string)
print(json_output)
```

## ⚡ Async Usage

For non-blocking operations in async applications, use `AsyncToonConverter`:

```python
import asyncio
from toon_parse import AsyncToonConverter

async def main():
    data = {"name": "Alice", "age": 30}
    
    # Async conversion
    toon_string = await AsyncToonConverter.from_json(data)
    print(toon_string)
    
    # Async parsing
    json_output = await AsyncToonConverter.to_json(toon_string)
    print(json_output)

asyncio.run(main())
```

## 📚 API Reference

The Python API mirrors the JavaScript API with snake_case naming conventions.

- `ToonConverter.from_json(data)`
- `ToonConverter.to_json(toon_string)`
- `ToonConverter.from_yaml(yaml_string)`
- `ToonConverter.to_yaml(toon_string)`
- `ToonConverter.from_xml(xml_string)`
- `ToonConverter.to_xml(toon_string)`
- `ToonConverter.from_csv(csv_string)`
- `ToonConverter.to_csv(toon_string)`
- `ToonConverter.validate(toon_string)`
- `AsyncToonConverter.*` (same methods as above, but async)

## 📄 License

MIT License
