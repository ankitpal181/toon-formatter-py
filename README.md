# 🚀 TOON Converter (Python)

A lightweight library to convert between **TOON** (Token-Oriented Object Notation) and popular data formats (JSON, YAML, XML, CSV).

**Reduce your LLM token costs by up to 40%** using the TOON format!

- **Documentation**: https://toonformatter.net/docs.html?package=toon-parse
- **Source Code**: https://github.com/ankitpal181/toon-formatter-py
- **Bug Reports**: https://github.com/ankitpal181/toon-formatter-py/issues
- **POC Tool**: https://toonformatter.net/

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

#### `ToonConverter` (Synchronous)
**Constructor**: `ToonConverter(encryptor: Encryptor = None)`

All conversion methods accept an optional `conversion_mode` argument:
- `conversion_mode`: `"no_encryption"` (default), `"middleware"`, `"ingestion"`, `"export"`.

- `from_json(data, conversion_mode=...)`: Converts dict/list/string to TOON.
- `to_json(toon_string, return_json=True, conversion_mode=...)`: Converts TOON to Python/JSON.
- `from_xml`, `from_csv`, `from_yaml`, `to_xml`, `to_csv`, `to_yaml`: Equivalent methods.
- `validate(toon_string)`: **Static Method Only**. Validates TOON syntax. Does not support encryption.

#### `AsyncToonConverter` (Asynchronous)
**Constructor**: `AsyncToonConverter(encryptor: Encryptor = None)`

- Mirrors all `ToonConverter` methods as `async` functions (e.g., `await conv.from_json(...)`).
- Supports the same `conversion_mode` parameters for encryption pipelines.
- `validate(toon_string)`: **Static Method Only**. Async validation. No encryption support.

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
