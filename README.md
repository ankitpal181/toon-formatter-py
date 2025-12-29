# 🚀 TOON Converter (Python)

A lightweight library to convert between **TOON** (Token-Oriented Object Notation) and popular data formats (JSON, YAML, XML, CSV).

**Reduce your LLM token costs by up to 40%** using the TOON format!

- **Documentation**: https://toonformatter.net/docs.html?package=toon-parse
- **Source Code**: https://github.com/ankitpal181/toon-formatter-py
- **Bug Reports**: https://github.com/ankitpal181/toon-formatter-py/issues
- **POC Tool**: https://toonformatter.net/

```bash
pip install toon-parse
```

## 🛠️ CLI Utility (New!)

Convert data and validate formats directly from your terminal using the unified `toon-parse` command.

### Features
- **Streamlined**: Single command for all conversion types.
- **Piping**: Full support for `stdin` and `stdout`.
- **Validation**: Standalone format validation logic.
- **Security**: Built-in support for all encryption modes.

### Usage Examples
```bash
# 1. Basic Conversion (JSON to TOON)
echo '{"name": "Alice"}' | toon-parse --from json --to toon

# 2. File-based Conversion with Async core
toon-parse --from xml --to json --input data.xml --output data.json --async

# 3. Secure Export (JSON to Encrypted XML)
toon-parse --from json --to xml --mode export --key <my_key> --input data.json

# 4. Format Validation
toon-parse --validate toon --input my_data.toon
```

## 🔄 Unified Format Converters (New!)

Beyond TOON, you can now convert directly between **JSON**, **YAML**, **XML**, and **CSV** using dedicated converter classes.

```python
from toon_parse import JsonConverter, YamlConverter, XmlConverter, CsvConverter

# JSON <-> XML
xml_output = JsonConverter.to_xml({"user": "Alice"})
json_output = XmlConverter.to_json(xml_output)

# CSV <-> YAML
yaml_output = CsvConverter.to_yaml("id,name\n1,Alice")
csv_output = YamlConverter.to_csv(yaml_output)
```

### Key Features
- **Direct Conversion**: No need to convert to TOON first.
- **Mixed Text Support**: `from_json`, `from_xml`, and `from_csv` methods automatically extract data from unstructured text.
- **Return Types**:
  - `JsonConverter.from_toon` and `from_yaml` support `return_json=True` (default) to return a JSON string, or `False` to return a dict/list.
  - `YamlConverter.to_json` supports `return_json=True` (default) to return a JSON string.
  - All other methods return **strings** (formatted xml, csv, yaml, etc.).

### 🔐 Using Encryption with Unified Converters

All new converters support the secure middleware pattern. Use the instance-based approach:

```python
from toon_parse import JsonConverter, Encryptor

# 1. Setup Encryptor
enc = Encryptor(algorithm='fernet', key=my_key)

# 2. Initialize Converter with Encryptor
converter = JsonConverter(encryptor=enc)

# 3. Convert with security mode
# Example: Decrypt input JSON -> convert to XML -> Encrypt output
encrypted_xml = converter.to_xml(
    encrypted_json_input, 
    conversion_mode="middleware"
)
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

### Mixed Text Support

The library can automatically extract and convert JSON, XML, and CSV data embedded within normal text. This is perfect for processing LLM outputs.

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

### 🔐 Secure Conversion Middleware (New!)

The `ToonConverter` can act as a **secure middleware** for processing encrypted data streams (e.g., from microservices). It handles the full **Decrypt -> Convert -> Encrypt** pipeline internally.

#### Supported Algorithms
- **Fernet**: High security (AES-128). Requires `cryptography`.
- **XOR**: Lightweight obfuscation.
- **Base64**: Encoding only.

#### Conversion Modes
1.  **`"middleware"`**: Encrypted Input → Encrypted Output (Decrypt → Convert → Re-encrypt)
2.  **`"ingestion"`**: Encrypted Input → Plain Output (Decrypt → Convert)
3.  **`"export"`**: Plain Input → Encrypted Output (Convert → Encrypt)
4.  **`"no_encryption"`**: Standard conversion (default)

#### Example Workflow

```python
from toon_parse import ToonConverter, Encryptor
from cryptography.fernet import Fernet

# Setup
key = Fernet.generate_key()
enc = Encryptor(key=key, algorithm='fernet')
converter = ToonConverter(encryptor=enc)

# --- Mode 1: Middleware (Encrypted -> Encrypted) ---
raw_data = '{"user": "Alice", "role": "admin"}'
encrypted_input = enc.encrypt(raw_data)  # Simulate upstream encrypted data

# Converter decrypts, converts to TOON, and re-encrypts
encrypted_toon = converter.from_json(
    encrypted_input, 
    conversion_mode="middleware"
)
print(f"Secure Result: {encrypted_toon}")

# --- Mode 2: Ingestion (Encrypted -> Plain) ---
plain_toon = converter.from_json(
    encrypted_input,
    conversion_mode="ingestion"
)
print(f"Decrypted TOON: {plain_toon}")

# --- Mode 3: Export (Plain -> Encrypted) ---
my_data = {"status": "ok"}
secure_packet = converter.from_json(
    my_data,
    conversion_mode="export"
)
print(f"Encrypted Output: {secure_packet}")
```

## ⚡ Async Usage

For non-blocking operations in async applications (e.g., FastAPI), use `AsyncToonConverter`.

```python
import asyncio
from toon_parse import AsyncToonConverter, Encryptor

async def main():
    # 1. Standard Async Usage
    converter = AsyncToonConverter()
    text = 'Data: <user><name>Alice</name></user>'
    toon = await converter.from_xml(text)
    print(toon)

    # 2. Async with Secure Middleware
    enc = Encryptor(algorithm='base64')
    secure_converter = AsyncToonConverter(encryptor=enc)
    
    # Decrypt -> Convert -> Encrypt (Middleware Mode)
    encrypted_msg = "eyJrZXkiOiAidmFsIn0=" # Base64 for {"key": "val"}
    
    # Use conversion_mode to specify pipeline behavior
    result = await secure_converter.from_json(
        encrypted_msg, 
        conversion_mode="middleware"
    )
    print(result)

asyncio.run(main())
```

## 📚 Features & Support

| Feature | JSON | XML | CSV | YAML | TOON |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Python Dict/List Input** | ✅ | N/A | N/A | N/A | N/A |
| **Pure String Input** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Mixed Text Support** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Async Support** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Encryption Support** | ✅ | ✅ | ✅ | ✅ | ✅ |

- **Mixed Text**: Finds occurrences of data formats in text (JSON, XML, CSV) and converts them in-place.
- **Encryption**: Supports Fernet, XOR, and Base64 middleware conversions.

## ⚙️ Static vs Instance Usage

### Conversion Methods (`from_json`, `to_json`, etc.)

All conversion methods support **both static and instance** calling patterns:

```python
from toon_parse import ToonConverter

# ✅ Static Usage (No Encryption)
toon = ToonConverter.from_json({"key": "value"})

# ✅ Instance Usage (Encryption Supported)
converter = ToonConverter(encryptor=enc)
toon = converter.from_json({"key": "value"}, conversion_mode="export")
```

**Important**: 
- **Static calls** (`ToonConverter.from_json(...)`) work but **cannot use encryption features**.
- **Instance calls** are required to use `conversion_mode` and encryption middleware.

The same applies to async methods.

### Validate Method

The `validate()` method is **strictly static** and does **not** support encryption:

```python
# ✅ Correct Usage
result = ToonConverter.validate('key: "value"')

# ❌ Will NOT work with encryption
converter = ToonConverter(encryptor=enc)
result = converter.validate(encrypted_data)  # No decryption happens!
```

**Why?** Validation returns a dictionary (not a string), which cannot be encrypted. If you need to validate encrypted data, decrypt it first manually:

```python
decrypted = enc.decrypt(encrypted_toon)
result = ToonConverter.validate(decrypted)
```

The same applies to `AsyncToonConverter.validate()`.

## 🛠 API Reference

### Core Converters

#### `ToonConverter` (Legacy & Easy Use)
- **Static & Instance**.
- Central hub for converting **TOON <-> Any Format**.

#### `JsonConverter`
- **Focus**: JSON <-> Any Format.
- `from_toon(..., return_json=True)`
- `from_yaml(..., return_json=True)`
- `to_xml`, `to_csv`, `to_yaml`, `to_toon`

#### `YamlConverter`
- **Focus**: YAML <-> Any Format.
- `to_json(..., return_json=True)`
- `from_json`, `from_xml`, `from_csv`, `from_toon`

#### `XmlConverter`
- **Focus**: XML <-> Any Format.
- `to_json` (returns JSON string), `from_json`, etc.

#### `CsvConverter`
- **Focus**: CSV <-> Any Format.
- `to_json` (returns JSON string), `from_json`, etc.

**Note**: All `to_csv` methods return a string. If the input is nested JSON/Object, it will be automatically **flattened** (e.g., `user.name`) to fit the CSV format. Conversely, `from_csv` will **unflatten** dotted keys back into objects.

### Async Converters
Mirroring the synchronous classes, we have:
- `AsyncJsonConverter`
- `AsyncYamlConverter`
- `AsyncXmlConverter`
- `AsyncCsvConverter`

Usage is identical, just use `await`.

### Encryption

#### `Encryptor`
**Constructor**: `Encryptor(key=None, algorithm='fernet')`
- `algorithm`: `'fernet'` (default), `'xor'`, `'base64'`.
- `key`: Required for Fernet/XOR.
- `encrypt(data)`, `decrypt(data)`: Helper methods.

### Utility Functions

```python
from toon_parse import extract_json_from_string, extract_xml_from_string, extract_csv_from_string
# Direct access to extraction logic without conversion
```

## 📄 License

MIT License
