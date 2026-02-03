# 🚀 TOON Converter (Python)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10 | 3.11 | 3.12 | 3.13](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12%20|%203.13-blue.svg)](https://www.python.org/downloads/)
[![LLM APIs cost reduction](https://img.shields.io/badge/LLM%20APIs-Up%20to%2040%25%20cost%20reduction-orange)](https://toonformatter.net/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/toon-parse?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=GREEN&left_text=Downloads)](https://pepy.tech/projects/toon-parse)

A powerful context reduction tool centered around converting data (JSON, YAML, XML, CSV) to **TOON** (Token-Oriented Object Notation) format for efficient LLM interactions.

**Reduce your LLM token costs by up to 40%** using the TOON format!

- **Documentation**: https://toonformatter.net/docs.html?package=toon-parse
- **Source Code**: https://github.com/ankitpal181/toon-formatter-py
- **Bug Reports**: https://github.com/ankitpal181/toon-formatter-py/issues
- **POC Tool**: https://toonformatter.net/

```bash
pip install toon-parse
```

## 🛠️ CLI Utility

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

## 🔄 Unified Format Converters

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

### 🧠 Smart Code Optimization (New!)

The library includes an intelligent **Data Manager** that preprocesses input to handle code blocks efficiently.

-   **Code Preservation**: Code snippets (detected via heuristics) are identified and protected from conversion logic.
-   **Context Reduction**: Code blocks are automatically optimized to reduce token usage by:
    -   Removing comments (`# ...`, `// ...`).
    -   Compressing double newlines to single newlines.
    -   Stripping unnecessary whitespace.

This ensures that while your data is converted to TOON for efficiency, any embedded code remains syntactically valid but token-optimized.

### 📉 Context Optimization (Expensive Words) (New!)

The library automatically identifies and replaces common "expensive" phrases with token-efficient alternatives to reduce the overall payload size required for LLM input.

> **Note**: While most alterations significantly reduce token count, some replacements may only reduce character count while keeping the token count the same. This still helps in reducing the API payload size (in bytes), which can reduce latency and cost for bandwidth-constrained environments.

**Examples:**
-   `"large language model"` → `"llm"`
-   `"frequently asked questions"` → `"faq"`
-   `"as soon as possible"` → `"asap"`
-   `"do not"` → `"don't"`
-   `"I am"` → `"i'm"`

This feature is **case-insensitive** and ensures that words inside code blocks and data blocks are **NOT** altered.

### 🔐 Secure Conversion Middleware

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


## 📦 Batch Processing

Process multiple data items concurrently using batch converters. Available for all formats: **TOON**, **JSON**, **YAML**, **XML**, and **CSV**.

### Synchronous Batch Converters

```python
from toon_parse import BatchToonConverter, BatchJsonConverter, BatchYamlConverter

# Process multiple items in parallel
converter = BatchToonConverter()

json_list = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]

# Convert all items to TOON (runs in parallel)
toon_results = converter.from_json(json_list, parallel=True)
print(len(toon_results))  # 3

# Convert back to JSON
json_results = converter.to_json(toon_results, parallel=True, return_json=False)
# Returns list of dicts
```

### Available Batch Converters

All batch converters support the same methods as their non-batch counterparts:

```python
from toon_parse import (
    BatchToonConverter,   # TOON ↔ JSON/YAML/XML/CSV
    BatchJsonConverter,   # JSON ↔ TOON/YAML/XML/CSV
    BatchYamlConverter,   # YAML ↔ TOON/JSON/XML/CSV
    BatchXmlConverter,    # XML ↔ TOON/JSON/YAML/CSV
    BatchCsvConverter     # CSV ↔ TOON/JSON/YAML/XML
)

# Example: Cross-format batch conversion
yaml_converter = BatchYamlConverter()
xml_converter = BatchXmlConverter()

yaml_list = ["name: Alice", "name: Bob", "name: Charlie"]

# YAML → XML (batch)
xml_results = yaml_converter.to_xml(yaml_list, parallel=True)

# XML → JSON (batch)
json_results = xml_converter.to_json(xml_results, parallel=True)
```

### Batch Validation

```python
from toon_parse import BatchToonConverter

# Validate multiple TOON strings
toon_list = [
    "name: Alice\nage: 30",
    "invalid toon",
    "name: Bob\nage: 25"
]

results = BatchToonConverter.validate(toon_list, parallel=True)

for i, result in enumerate(results):
    print(f"Item {i}: {'✅ Valid' if result['is_valid'] else '❌ Invalid'}")
```

### Batch with Encryption

```python
from toon_parse import BatchJsonConverter, Encryptor
from cryptography.fernet import Fernet

key = Fernet.generate_key()
enc = Encryptor(key=key, algorithm='fernet')
converter = BatchJsonConverter(encryptor=enc)

# Encrypt multiple JSON strings
json_list = ['{"id": 1}', '{"id": 2}', '{"id": 3}']
encrypted_inputs = [enc.encrypt(j) for j in json_list]

# Batch convert with middleware mode (decrypt → convert → encrypt)
encrypted_toon = converter.to_toon(
    encrypted_inputs,
    conversion_mode="middleware",
    parallel=True
)
```

## ⚡ Async Batch Processing

For high-performance non-blocking batch operations, use async batch converters. These use `asyncio.gather` for implicit parallelism.

### Key Features
- **Implicit Parallelism**: No `parallel` flag needed - concurrency is automatic via `asyncio.gather`
- **Non-blocking I/O**: All file operations use thread pool executors
- **Event Loop Friendly**: Doesn't block the event loop during batch processing

### Basic Usage

```python
import asyncio
from toon_parse import AsyncBatchToonConverter, AsyncBatchJsonConverter

async def main():
    converter = AsyncBatchToonConverter()
    
    # Process 100 items concurrently
    json_list = [{"id": i, "name": f"User{i}"} for i in range(100)]
    
    # Automatically runs all conversions concurrently
    toon_results = await converter.from_json(json_list)
    
    print(f"Converted {len(toon_results)} items")

asyncio.run(main())
```

### Available Async Batch Converters

```python
from toon_parse import (
    AsyncBatchToonConverter,   # TOON ↔ JSON/YAML/XML/CSV
    AsyncBatchJsonConverter,   # JSON ↔ TOON/YAML/XML/CSV
    AsyncBatchYamlConverter,   # YAML ↔ TOON/JSON/XML/CSV
    AsyncBatchXmlConverter,    # XML ↔ TOON/JSON/YAML/CSV
    AsyncBatchCsvConverter     # CSV ↔ TOON/JSON/YAML/XML
)
```

### Cross-Format Async Batch Pipeline

```python
import asyncio
from toon_parse import AsyncBatchJsonConverter, AsyncBatchYamlConverter

async def convert_pipeline():
    json_conv = AsyncBatchJsonConverter()
    yaml_conv = AsyncBatchYamlConverter()
    
    # Start with 50 JSON objects
    json_data = [{"user": f"user{i}", "active": True} for i in range(50)]
    
    # JSON → YAML (concurrent)
    yaml_results = await json_conv.to_yaml(json_data)
    
    # YAML → TOON (concurrent)
    toon_results = await yaml_conv.to_toon(yaml_results)
    
    return toon_results

results = asyncio.run(convert_pipeline())
```

### Concurrent Multi-Format Processing

```python
import asyncio
from toon_parse import (
    AsyncBatchJsonConverter,
    AsyncBatchYamlConverter,
    AsyncBatchXmlConverter
)

async def process_all_formats():
    # Initialize converters
    json_conv = AsyncBatchJsonConverter()
    yaml_conv = AsyncBatchYamlConverter()
    xml_conv = AsyncBatchXmlConverter()
    
    # Different format data
    json_data = [{"id": 1}, {"id": 2}]
    yaml_data = ["name: Alice", "name: Bob"]
    xml_data = ["<user>Alice</user>", "<user>Bob</user>"]
    
    # Process all formats concurrently
    results = await asyncio.gather(
        json_conv.to_toon(json_data),
        yaml_conv.to_toon(yaml_data),
        xml_conv.to_toon(xml_data)
    )
    
    json_toon, yaml_toon, xml_toon = results
    return json_toon, yaml_toon, xml_toon

asyncio.run(process_all_formats())
```

### Async Batch Validation

```python
import asyncio
from toon_parse import AsyncBatchToonConverter

async def validate_batch():
    toon_list = [
        "name: Alice\nage: 30",
        "invalid toon data",
        "name: Bob\nage: 25"
    ]
    
    # Concurrent validation
    results = await AsyncBatchToonConverter.validate(toon_list)
    
    for i, result in enumerate(results):
        status = "✅ Valid" if result['is_valid'] else "❌ Invalid"
        print(f"Item {i}: {status}")

asyncio.run(validate_batch())
```

### Async Batch with Encryption

```python
import asyncio
from toon_parse import AsyncBatchJsonConverter, Encryptor
from cryptography.fernet import Fernet

async def secure_batch_processing():
    key = Fernet.generate_key()
    enc = Encryptor(key=key, algorithm='fernet')
    converter = AsyncBatchJsonConverter(encryptor=enc)
    
    # Prepare encrypted inputs
    json_list = ['{"user": "Alice"}', '{"user": "Bob"}', '{"user": "Charlie"}']
    encrypted_inputs = [enc.encrypt(j) for j in json_list]
    
    # Batch convert with middleware (decrypt → convert → encrypt)
    # All items processed concurrently
    encrypted_yaml = await converter.to_yaml(
        encrypted_inputs,
        conversion_mode="middleware"
    )
    
    return encrypted_yaml

asyncio.run(secure_batch_processing())
```

### Performance Comparison

```python
import asyncio
import time
from toon_parse import BatchToonConverter, AsyncBatchToonConverter

# Generate test data
data = [{"id": i, "value": f"test{i}"} for i in range(200)]

# Synchronous batch (with parallel=True)
start = time.perf_counter()
sync_converter = BatchToonConverter()
sync_results = sync_converter.from_json(data, parallel=True)
sync_time = time.perf_counter() - start

# Async batch (implicit parallelism)
async def async_convert():
    converter = AsyncBatchToonConverter()
    return await converter.from_json(data)

start = time.perf_counter()
async_results = asyncio.run(async_convert())
async_time = time.perf_counter() - start

print(f"Sync batch: {sync_time:.2f}s")
print(f"Async batch: {async_time:.2f}s")
# Async is typically 20-30% faster and doesn't block the event loop
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
