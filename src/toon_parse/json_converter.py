from .utils import format_value, parse_value, split_by_delimiter, extract_json_from_string
from .validator import validate_toon_string
import re, json

def json_to_toon_parser(data, key='', depth=0):
    """
    Converts JSON-compatible data to TOON format.
    """
    indent = '  ' * depth
    next_indent = '  ' * (depth + 1)

    # ---- Primitive ----
    if data is None or not isinstance(data, (dict, list)):
        if key:
            return f"{indent}{key}: {format_value(data)}"
        return f"{indent}{format_value(data)}"

    # ---- Array ----
    if isinstance(data, list):
        length = len(data)

        # Empty array
        if length == 0:
            return f"{indent}{key}[0]:"

        # Array of primitives
        # Check if first item is primitive (not dict/list)
        first_item = data[0]
        if not isinstance(first_item, (dict, list)) or first_item is None:
            values = ", ".join(format_value(v) for v in data)
            return f"{indent}{key}[{length}]: {values}"

        # ---- Array of objects ----
        # Determine if all fields in object are primitives
        # In Python, we need to be careful if data[0] is not a dict
        if isinstance(first_item, dict):
            fields = list(first_item.keys())
            
            # Check if all rows are dicts and have primitive values for these fields
            is_tabular = True
            for row in data:
                if not isinstance(row, dict):
                    is_tabular = False
                    break
                for f in fields:
                    val = row.get(f)
                    # Check if value is primitive
                    if isinstance(val, (dict, list)) and val is not None:
                        is_tabular = False
                        break
                if not is_tabular:
                    break
            
            # ---- TABULAR ARRAY (structured array) ----
            if is_tabular:
                header = ",".join(fields)
                lines = []
                lines.append(f"{indent}{key}[{length}]{{{header}}}:")

                for row in data:
                    row_vals = []
                    for f in fields:
                        row_vals.append(format_value(row.get(f)))
                    lines.append(f"{next_indent}{','.join(row_vals)}")

                return "\n".join(lines)

        # ---- YAML-STYLE ARRAY (nested objects present or mixed types) ----
        lines = []
        lines.append(f"{indent}{key}[{length}]:")

        for row in data:
            lines.append(f"{next_indent}-") # item marker
            if isinstance(row, dict):
                for f, child in row.items():
                    block = json_to_toon_parser(child, f, depth + 2)
                    lines.append(block)
            elif isinstance(row, list):
                 # Handle list inside list if needed, though TOON usually expects objects here
                 # We'll just recurse with empty key
                 block = json_to_toon_parser(row, "", depth + 2)
                 lines.append(block)
            else:
                 # Primitive in mixed array?
                 lines.append(f"{'  ' * (depth + 2)}{format_value(row)}")

        return "\n".join(lines)

    # ---- Object ----
    lines = []
    if key:
        lines.append(f"{indent}{key}:")
    
    # If key is empty (root), we don't indent children further relative to current depth
    child_depth = depth + 1 if key else depth

    for child_key, child_val in data.items():
        block = json_to_toon_parser(child_val, child_key, child_depth)
        lines.append(block)

    return "\n".join(lines)


def toon_to_json(toon_string, return_json=False):
    """
    Converts TOON string to JSON-compatible data.
    """
    # Validate TOON string before conversion
    validation_status = validate_toon_string(toon_string)

    if not validation_status['is_valid']:
        raise ValueError(f'Invalid TOON: {validation_status["error"]}')

    lines = toon_string.split('\n')
    root = {}
    stack = []

    # Pre-process: Check for Root Array or Root Primitive
    # Find first non-empty line
    first_line = next((l for l in lines if l.strip()), None)
    if not first_line:
        return {}

    # Root Array detection
    if first_line.strip().startswith('['):
        root = []
        stack.append({'obj': root, 'indent': 0, 'is_root_array': True})
    else:
        # Root object container
        # In JS: stack.push({ obj: root, indent: -1 });
        stack.append({'obj': root, 'indent': -1})

    tabular_headers = None
    tabular_target = None
    tabular_indent = -1
    tabular_delimiter = ','

    for line in lines:
        if not line.strip():
            continue

        # Calculate indent
        indent_match = re.match(r'^(\s*)', line)
        indent = len(indent_match.group(1)) if indent_match else 0
        trimmed = line.strip()

        # --- Tabular Data Handling ---
        if tabular_target is not None:
            if tabular_indent == -1:
                if indent > stack[-1]['indent']:
                    tabular_indent = indent
                else:
                    tabular_target = None
                    tabular_headers = None
            
            if tabular_target is not None and indent == tabular_indent:
                values = split_by_delimiter(trimmed, tabular_delimiter)
                # Map values using parse_value
                values = [parse_value(v) for v in values]
                
                row_obj = {}
                # Zip headers and values
                for h, v in zip(tabular_headers, values):
                    row_obj[h] = v
                tabular_target.append(row_obj)
                continue
            elif tabular_target is not None and indent < tabular_indent:
                tabular_target = None
                tabular_headers = None
                tabular_indent = -1

        # Adjust stack
        while len(stack) > 1 and stack[-1]['indent'] >= indent:
            stack.pop()

        parent = stack[-1]['obj']

        # Root Array Header check
        if len(stack) == 1 and stack[0].get('is_root_array') and trimmed.startswith('['):
            # Regex: ^\[(\d+)(.*?)\](?:\{(.*?)\})?:\s*(.*)$
            root_match = re.match(r'^\[(\d+)(.*?)\](?:\{(.*?)\})?:\s*(.*)$', trimmed)
            if root_match:
                # delim_char = root_match.group(2)
                # fields_str = root_match.group(3)
                # rest = root_match.group(4) (not used in JS for root header logic?)
                
                delim_char = root_match.group(2)
                fields_str = root_match.group(3)
                
                delimiter = ','
                if delim_char == '\\t': delimiter = '\t'
                elif delim_char == '|': delimiter = '|'
                
                if fields_str:
                    tabular_headers = [s.strip() for s in fields_str.split(',')]
                    tabular_target = root
                    tabular_indent = -1
                    tabular_delimiter = delimiter
            continue

        # --- List Item Handling (-) ---
        if trimmed.startswith('-'):
            content = trimmed[1:].strip()

            if content == '':
                new_obj = {}
                parent.append(new_obj)
                stack.append({'obj': new_obj, 'indent': indent})
                continue
            else:
                # Try KV match: ^(.+?):\s*(.*)$
                kv_match = re.match(r'^(.+?):\s*(.*)$', content)
                # Try Array match: ^\[(\d+)(.*?)\](?:\{(.*?)\})?:\s*(.*)$
                array_match = re.match(r'^\[(\d+)(.*?)\](?:\{(.*?)\})?:\s*(.*)$', content)

                if array_match:
                    # length = int(array_match.group(1))
                    delim_char = array_match.group(2) or ','
                    delimiter = '\t' if delim_char == '\\t' else ('|' if delim_char == '|' else ',')
                    fields_str = array_match.group(3)
                    rest = array_match.group(4)

                    new_array = []
                    parent.append(new_array)

                    if fields_str:
                        tabular_headers = [s.strip() for s in fields_str.split(',')]
                        tabular_target = new_array
                        tabular_indent = -1
                        tabular_delimiter = delimiter
                    elif rest:
                        values = split_by_delimiter(rest, delimiter)
                        new_array.extend([parse_value(v) for v in values])
                    else:
                        stack.append({'obj': new_array, 'indent': indent + 1})
                    continue

                if kv_match:
                    key = kv_match.group(1).strip()
                    val_str = kv_match.group(2).strip()
                    new_obj = {}

                    if val_str == '':
                        new_obj[key] = {}
                        parent.append(new_obj)
                        stack.append({'obj': new_obj[key], 'indent': indent + 1})
                    else:
                        new_obj[key] = parse_value(val_str)
                        parent.append(new_obj)
                        # In JS: stack.push({ obj: newObj, indent: indent });
                        # Wait, if it's a one-line KV inside a list item, why push to stack?
                        # Ah, because subsequent lines might be children of this object?
                        # But indent is same as current line.
                        stack.append({'obj': new_obj, 'indent': indent})
                    continue

                parent.append(parse_value(content))
                continue

        # --- Key-Value or Array Header Handling ---
        # arrayHeaderMatch = trimmed.match(/^(.+?)\[(\d+)(.*?)\](?:\{(.*?)\})?:\s*(.*)$/);
        array_header_match = re.match(r'^(.+?)\[(\d+)(.*?)\](?:\{(.*?)\})?:\s*(.*)$', trimmed)

        if array_header_match:
            key = array_header_match.group(1).strip()
            # length = int(array_header_match.group(2))
            delim_char = array_header_match.group(3)
            fields_str = array_header_match.group(4)
            value_str = array_header_match.group(5)

            delimiter = ','
            if delim_char == '\\t': delimiter = '\t'
            elif delim_char == '|': delimiter = '|'

            new_array = []
            
            if isinstance(parent, dict):
                parent[key] = new_array
            # If parent is list? Should not happen here unless malformed TOON
            
            if fields_str:
                tabular_headers = [s.strip() for s in fields_str.split(',')]
                tabular_target = new_array
                tabular_indent = -1
                tabular_delimiter = delimiter
            elif value_str and value_str.strip() != '':
                values = split_by_delimiter(value_str, delimiter)
                new_array.extend([parse_value(v) for v in values])
            else:
                stack.append({'obj': new_array, 'indent': indent + 1})
            continue

        # Standard Key-Value: key: value
        kv_match = re.match(r'^(.+?):\s*(.*)$', trimmed)
        if kv_match:
            key = kv_match.group(1).strip()
            val_str = kv_match.group(2).strip()

            if isinstance(parent, dict):
                if val_str == '':
                    new_obj = {}
                    parent[key] = new_obj
                    stack.append({'obj': new_obj, 'indent': indent + 1})
                else:
                    parent[key] = parse_value(val_str)
            continue

    return json.dumps(root) if return_json else root



def json_to_toon(data, key='', depth=0):
    # Handle string input (JSON text or mixed text)
    if isinstance(data, str):
        converted_text = data
        iteration_count = 0
        max_iterations = 100
        found_any_json = False

        while iteration_count < max_iterations:
            json_block = extract_json_from_string(converted_text)
            if not json_block: break
            
            found_any_json = True
            try:
                toon_string = json_to_toon_parser(json.loads(json_block), key, depth)
                toon_output = toon_string.strip()
                converted_text = converted_text.replace(json_block, toon_output)
                iteration_count += 1
            except:
                raise Exception('Error while converting JSON to TOON')

        # If no JSON was found, treat the string as a primitive value
        if not found_any_json:
            return json_to_toon_parser(data, key, depth)
            
        return converted_text
    else:
        # Handle dict, list, or primitives
        return json_to_toon_parser(data, key, depth)

