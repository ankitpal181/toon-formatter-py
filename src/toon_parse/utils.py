import re

def encode_xml_reserved_chars(raw_xml_string):
    """
    Encodes XML reserved characters to prevent parsing errors.
    """
    if not isinstance(raw_xml_string, str):
        return ''
    
    # Replace & with &amp; but not if it's already an entity
    return re.sub(r'&(?!#|\w+;)', '&amp;', raw_xml_string)

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
    
    for i, line in enumerate(lines):
        comma_count = line.count(',')
        if comma_count > 0:
            start_line_index = i
            break
            
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
        result_lines.append(line)
        
    result = "\n".join(result_lines).strip()
    
    # Avoid matching TOON arrays (e.g. users[2]{id,name}:)
    if re.match(r'^\s*(\w+)?\[\d+\]', result):
        return None
        
    return result
