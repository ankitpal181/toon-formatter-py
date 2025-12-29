import re
import inspect

def encode_xml_reserved_chars(raw_xml_string):
    """
    Encodes XML reserved characters to prevent parsing errors.
    """
    if not isinstance(raw_xml_string, str):
        return ''
    
    # Replace & with &amp; but not if it's already an entity
    return re.sub(r'&(?!#|\w+;)', '&amp;', raw_xml_string)

def sanitize_tag_name(name):
    """
    Sanitizes a string for use as an XML tag name.
    """
    if not isinstance(name, str) or not name:
        return '_'
        
    # If name starts with non-letter/underscore (e.g. digit), prepend underscore
    if re.match(r'^[^a-zA-Z_]', name):
        name = '_' + name
        
    # Replace invalid chars with underscore
    # JS: return name.replace(/[^a-zA-Z0-9_.]/g, '_');
    return re.sub(r'[^a-zA-Z0-9_.]', '_', name)

def split_by_delimiter(text, delimiter):
    """
    Splits a string by delimiter while respecting quoted strings.
    """
    result = []
    current = []
    in_quote = False
    i = 0
    while i < len(text):
        char = text[i]
        if char == '"' and (i == 0 or text[i - 1] != '\\'):
            in_quote = not in_quote
        
        if char == delimiter and not in_quote:
            result.append("".join(current))
            current = []
        else:
            current.append(char)
        i += 1
    
    result.append("".join(current))
    return result

def parse_value(val):
    """
    Parses a value string into its correct Python type.
    """
    val = val.strip()
    if val == 'true':
        return True
    if val == 'false':
        return False
    if val == 'null':
        return None
    if val == '':
        return ""
    
    # Number check
    # Check for simple integer or float
    # Avoid treating '0123' as a number if we want to be strict, but JS version:
    # !isNaN(Number(val)) && val !== '' && !val.startsWith('0') && val !== '0'
    # JS version logic:
    # if val is '0' -> 0
    # if val starts with '0' but not '0.' -> string (e.g. '0123')
    
    if val == '0':
        return 0
    
    try:
        # Try float first to catch everything
        num = float(val)
        # Check leading zeros for non-decimals
        if val.startswith('0') and '.' not in val and len(val) > 1:
             # It's a string like "0123"
             pass
        else:
            # If it's an integer, return int
            if num.is_integer() and '.' not in val:
                return int(num)
            return num
    except ValueError:
        pass

    # String unquoting
    if val.startswith('"') and val.endswith('"'):
        # Remove surrounding quotes and unescape internal quotes
        # JS: .replace(/\\"/g, '"').replace(/\\\\/g, '\\')
        inner = val[1:-1]
        return inner.replace('\\"', '"').replace('\\\\', '\\')
    
    return val

def format_value(v):
    """
    Formats a value according to TOON rules.
    """
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, str):
        # Escape quotes
        escaped = v.replace('"', '\\"')
        return f'"{escaped}"'
    return str(v)

def extract_json_from_string(text):
    """
    Extracts JSON from mixed text.
    """
    if not text or not isinstance(text, str):
        return None
    
    start_index = -1
    for i, char in enumerate(text):
        if char == '{' or char == '[':
            # Ignore if preceded by non-whitespace (e.g. key[2]), unless it's a closing bracket/brace or XML tag end
            # JS: if (i > 0 && /\S/.test(text[i - 1]) && !/[\}\]>]/.test(text[i - 1]))
            if i > 0:
                prev_char = text[i-1]
                if not prev_char.isspace() and prev_char not in ('}', ']', '>'):
                    continue
            
            start_index = i
            break
            
    if start_index == -1:
        return None
        
    balance = 0
    in_quote = False
    escape = False
    
    for i in range(start_index, len(text)):
        char = text[i]
        
        if escape:
            escape = False
            continue
            
        if char == '\\':
            escape = True
            continue
            
        if char == '"':
            in_quote = not in_quote
            continue
            
        if not in_quote:
            if char == '{' or char == '[':
                balance += 1
            elif char == '}' or char == ']':
                balance -= 1
            
            if balance == 0:
                candidate = text[start_index:i+1]
                
                # Avoid matching TOON arrays (e.g. [3]: 1, 2, 3)
                if re.match(r'^\s*\[\d+\]', candidate):
                    # Continue searching for next JSON block
                    start_index = -1
                    for j in range(i+1, len(text)):
                        if text[j] == '{' or text[j] == '[':
                            start_index = j
                            break
                    if start_index == -1:
                        return None
                    balance = 0
                    in_quote = False
                    escape = False
                    continue
                
                try:
                    import json
                    json.loads(candidate)
                    return candidate
                except json.JSONDecodeError:
                    pass
                    
    return None

def extract_xml_from_string(text):
    """
    Extracts XML from mixed text.
    """
    if not text or not isinstance(text, str):
        return None
        
    # Find first start tag (including self-closing)
    start_tag_regex = re.compile(r'<([a-zA-Z0-9_:-]+)(?:\s[^>]*)?\/?>')
    match = start_tag_regex.search(text)
    
    if not match:
        return None
        
    start_index = match.start()
    root_tag_name = match.group(1)
    full_match = match.group(0)
    
    if full_match.endswith('/>'):
        return full_match
        
    balance = 0
    tag_regex = re.compile(r'<\/?([a-zA-Z0-9_:-]+)(?:\s[^>]*)?\/?>')
    
    # We need to iterate through matches starting from start_index
    for match_tag in tag_regex.finditer(text, start_index):
        full_tag = match_tag.group(0)
        tag_name = match_tag.group(1)
        
        if tag_name != root_tag_name:
            continue
            
        if full_tag.startswith('</'):
            balance -= 1
        elif not full_tag.endswith('/>'):
            balance += 1
            
        if balance == 0:
            return text[start_index:match_tag.end()]
            
    return None

def extract_csv_from_string(text):
    """
    Extracts CSV from mixed text.
    """
    if not text or not isinstance(text, str):
        return None
        
    lines = text.split('\n')
    start_line_index = -1
    
    start_line_index = -1
    
    def is_json_like(line):
        trimmed = line.strip()
        # "key": value
        if re.search(r'^"[^"]+"\s*:', trimmed): return True
        # { or [ start
        if re.search(r'^[\{\[]', trimmed): return True
        # } or ] end (with optional comma)
        if re.search(r'^[\}\]],?$', trimmed): return True
        return False
        
    def is_yaml_like(line):
        trimmed = line.strip()
        # - value
        if trimmed.startswith('- '): return True
        # Key: Value (heuristic) - avoid CSV-like
        if re.search(r'^[^",]+:\s', trimmed): return True
        return False
        
    def is_xml_like(line):
        trimmed = line.strip()
        return trimmed.startswith('<') and '>' in trimmed

    def is_toon_structure(line):
        trimmed = line.strip()
        # [N]... or key[N]... ending with :
        return re.search(r'^.*?\[\d+\].*:\s*$', trimmed)

    # First pass: find start
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check TOON header
        if is_toon_structure(line):
            count_match = re.search(r'\[(\d+)\]', line)
            count = int(count_match.group(1)) if count_match else 0
            i += count + 1 # Skip header + content? 
            # In JS: i += count. Loop increments i.
            # So here: i += count is safe if we continue immediately.
            continue
            
        comma_count = line.count(',')
        if comma_count > 0:
            if not (is_json_like(line) or is_yaml_like(line) or is_xml_like(line)):
                start_line_index = i
                break
        i += 1
            
    if start_line_index == -1:
        return None
        
    result_lines = []
    
    for i in range(start_line_index, len(lines)):
        line = lines[i]
        if not line.strip():
            continue
            
        comma_count = line.count(',')
        if comma_count == 0:
            break
            
        # JS Stop condition
        if is_json_like(line) or is_yaml_like(line) or is_xml_like(line):
            break
            
        result_lines.append(line)
        
    result = "\n".join(result_lines).strip()
    
    # Avoid matching TOON arrays (e.g. users[2]{id,name}:)
    if re.match(r'^\s*(\w+)?\[\d+\]', result):
        return None
        
    # Improved check from JS: 
    # Check for JSON-like start/end
    trimmed_res = result.strip()
    # JS: /^[\{\[]/.test(trimmed)
    if trimmed_res.startswith('{') or trimmed_res.startswith('['):
        return None
        
    return result

def flatten_json(data):
    """
    Flattens a JSON object/list for CSV conversion.
    """
    if isinstance(data, list):
        return [flatten_object(row) for row in data]
    elif isinstance(data, dict):
        return flatten_object(data)
    return {}

def flatten_object(obj, prefix='', result=None):
    """
    Recursively flattens an object.
    """
    if result is None:
        result = {}
        
    if obj is None:
        result[prefix] = None
        return result
        
    # Attempt to parse string if it looks like JSON
    if isinstance(obj, str):
        trimmed = obj.strip()
        if (trimmed.startswith('{') and trimmed.endswith('}')) or \
           (trimmed.startswith('[') and trimmed.endswith(']')):
            try:
                import json
                parsed = json.loads(obj)
                flatten_object(parsed, prefix, result)
                return result
            except:
                pass

    if isinstance(obj, dict):
        # Handle Date? Python datetime objects? Assuming inputs are mostly JSON-compatible types.
        for key, value in obj.items():
            new_key = f"{prefix}.{key}" if prefix else key
            flatten_object(value, new_key, result)
    elif isinstance(obj, list):
         # Handle list inside object? 
         # The JS version mainly handles Object recursion. 
         # For CSV, lists inside columns usually become JSON strings or similar.
         # But the JS code: 
         # Object.keys(obj).forEach... works on arrays too (indices as keys).
         for i, value in enumerate(obj):
             new_key = f"{prefix}.{i}" if prefix else str(i)
             flatten_object(value, new_key, result)
    else:
        # Primitive
        result[prefix] = obj
        
    return result

def unflatten_object(data):
    """
    Unflattens a JSON object (reverses flattening).
    """
    if not isinstance(data, dict) or data is None:
        return data
        
    # Check if keys imply flattening (contain dots)
    keys = list(data.keys())
    has_dot = any('.' in k for k in keys)
    
    if not has_dot:
        return data
        
    result = {}
    for key, value in data.items():
        parts = key.split('.')
        current = result
        for i, part in enumerate(parts[:-1]):
            # Check if part implies array index?
            # Python dicts are fine. We will produce dicts of dicts.
            # If we want arrays, we'd need to infer from keys "0", "1"...
            # The JS version uses: `r[e] || (r[e] = (keys.length - 1 === j ? data[i] : {}))`
            # It builds objects.
            
            if part not in current:
                current[part] = {}
            current = current[part]
            
        current[parts[-1]] = value
        
    return result

def get_function_signature_bindings(function, *args, **kwargs):
    try:
        sig = inspect.signature(function)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        return (bound.arguments, sig.parameters,)
    except TypeError:
        return (None, None)

def _populate_converter_arguments(function, *args, **kwargs):
    arguments, parameters = get_function_signature_bindings(function, *args, **kwargs)

    if arguments is None or len(parameters) < 2:
        # Original function will throw necessary errors
        raise TypeError("Invalid function signature")

    param_names = list(parameters.keys())    
    self = arguments.get('self')
    data_param_name = param_names[1]
    data = arguments.get(data_param_name)
    conversion_mode = arguments.get("conversion_mode")
    return_json = arguments.get("return_json")
    keyword_args = {
        k: v for k, v in arguments.items() 
        if k not in ('self', data_param_name)
    }
    
    return (self, data, conversion_mode, return_json, keyword_args)

def encryption_modulator(convertor_function):
    def encryption_wrapper(*args, **kwargs):
        first_arg = args[0] if args else None
        
        if hasattr(first_arg, 'encryptor'):
            # Instance Mode
            try:
                self, data, conversion_mode, return_json, keyword_args = _populate_converter_arguments(
                    convertor_function, *args, **kwargs
                )
                
                if self.encryptor and conversion_mode != "no_encryption":
                    if conversion_mode == "middleware":
                        decrypted_data = self.encryptor.decrypt(data)
                        plain_converted_data = convertor_function(self, decrypted_data, **keyword_args)
                        converted_data = self.encryptor.encrypt(plain_converted_data)
                    elif conversion_mode == "ingestion":
                        decrypted_data = self.encryptor.decrypt(data)
                        converted_data = convertor_function(self, decrypted_data, **keyword_args)
                    elif conversion_mode == "export":
                        plain_converted_data = convertor_function(*args, **kwargs)
                        converted_data = self.encryptor.encrypt(plain_converted_data)
                    else:
                        converted_data = convertor_function(*args, **kwargs)
                else:
                    converted_data = convertor_function(*args, **kwargs)

                return converted_data
            except TypeError as te:
                if str(te) == "Invalid function signature":
                    return convertor_function(*args, **kwargs)
                raise te
            except Exception as ex:
                if conversion_mode in ("middleware", "export") and return_json is False:
                    raise ValueError(
                        "return_json must be True for middleware and export conversion modes"
                    )
                raise ex
        else:
            # Static Mode
            return convertor_function(None, *args, **kwargs)

    return encryption_wrapper

def async_encryption_modulator(convertor_function):
    async def encryption_wrapper(*args, **kwargs):
        first_arg = args[0] if args else None
        
        if hasattr(first_arg, 'encryptor'):
            # Instance Mode
            try:
                self, data, conversion_mode, return_json, keyword_args = _populate_converter_arguments(
                    convertor_function, *args, **kwargs
                )

                if self.encryptor and conversion_mode != "no_encryption":
                    if conversion_mode == "middleware":
                        decrypted_data = self.encryptor.decrypt(data)
                        plain_converted_data = await convertor_function(self, decrypted_data, **keyword_args)
                        converted_data = self.encryptor.encrypt(plain_converted_data)
                    elif conversion_mode == "ingestion":
                        decrypted_data = self.encryptor.decrypt(data)
                        converted_data = await convertor_function(self, decrypted_data, **keyword_args)
                    elif conversion_mode == "export":
                        plain_converted_data = await convertor_function(*args, **kwargs)
                        converted_data = self.encryptor.encrypt(plain_converted_data)
                    else:
                        converted_data = await convertor_function(*args, **kwargs)
                else:
                    converted_data = await convertor_function(*args, **kwargs)

                return converted_data
            except TypeError as te:
                if str(te) == "Invalid function signature":
                    return await convertor_function(*args, **kwargs)
                raise te
            except Exception as ex:
                if conversion_mode in ("middleware", "export") and return_json is False:
                    raise ValueError(
                        "return_json must be True for middleware and export conversion modes"
                    )
                raise ex
        else:
            # Static Mode
            return await convertor_function(None, *args, **kwargs)

    return encryption_wrapper

def build_tag(key, value):
    if isinstance(value, dict):
        # We need to process children to separate attributes from content
        # But we can't easily separate them if we just recurse.
        # We should peek inside `value` for `@attributes`.
        key = sanitize_tag_name(key)
        attrs = ""
        content = ""
        
        # Process @attributes first
        if "@attributes" in value:
            attr_data = value["@attributes"]
            for k, v in attr_data.items():
                attrs += f' {k}="{v}"'
        
        # Process other keys
        for k, v in value.items():
            if k == "@attributes": continue
            if k == "#text":
                content += str(v)
            else:
                # Recurse
                if isinstance(v, list):
                    for item in v:
                        content += build_tag(k, item)
                else:
                    content += build_tag(k, v)
        
        return f"<{key}{attrs}>{content}</{key}>"
    
    elif value is not None:
        key = sanitize_tag_name(key)
        return f"<{key}>{value}</{key}>"
    else:
        key = sanitize_tag_name(key)
        return f"<{key} />"
