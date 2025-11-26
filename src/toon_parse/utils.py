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
