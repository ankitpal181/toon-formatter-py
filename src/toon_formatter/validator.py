import re
from .utils import split_by_delimiter

def validate_toon_string(toon_string):
    """
    Validates a TOON string for syntax and structural correctness.
    """
    if not toon_string or not isinstance(toon_string, str):
        return {'is_valid': False, 'error': 'Input must be a non-empty string.'}

    lines = toon_string.split('\n')
    # Stack of contexts: { indent, type: 'root'|'object'|'array', expected?, count? }
    context_stack = [{'indent': 0, 'type': 'root', 'count': 0}]
    line_number = 0

    # Regex Definitions
    REGEX = {
        'map_key': re.compile(r'^[^:\[]+:\s*$'),
        'array_key': re.compile(r'^[^:]+\[(\d+)([\t|])?\](?:\{[^}]+\})?:\s*(.*)$'),
        'root_array': re.compile(r'^\[(\d+)([\t|])?\](?:\{[^}]+\})?:\s*(.*)$'),
        'list_item': re.compile(r'^\-.*'),
        'list_item_empty': re.compile(r'^\-\s*$'),
        'key_value': re.compile(r'^[^:\[]+:\s*(?:".*?"|[^"].*)$'),
        'tabular_row': re.compile(r'^\s*[^:]+\s*$'),
    }

    is_inside_tabular_array = False

    def opens_new_block(trimmed_line):
        return (REGEX['map_key'].match(trimmed_line) or
                REGEX['array_key'].match(trimmed_line) or
                REGEX['root_array'].match(trimmed_line) or
                REGEX['list_item_empty'].match(trimmed_line))

    def starts_tabular(trimmed_line):
        is_array = REGEX['array_key'].match(trimmed_line) or REGEX['root_array'].match(trimmed_line)
        return is_array and '{' in trimmed_line and '}' in trimmed_line

    for raw_line in lines:
        line_number += 1
        line = raw_line.rstrip()

        if not line.strip() or line.strip().startswith('#'):
            continue

        trimmed_line = line.strip()
        
        # Calculate indentation
        match = re.search(r'\S', raw_line)
        current_indent = match.start() if match else len(raw_line)
        
        current_context = context_stack[-1]
        required_indent = current_context['indent']

        # --- Inline Array Validation ---
        array_match = REGEX['array_key'].match(trimmed_line) or REGEX['root_array'].match(trimmed_line)
        if array_match:
            size = int(array_match.group(1))
            delim_char = array_match.group(2)
            content = array_match.group(3)

            if content and content.strip() != '':
                # Inline Array: Validate immediately
                delimiter = ','
                if delim_char == '\\t': delimiter = '\t'
                elif delim_char == '|': delimiter = '|'

                items = split_by_delimiter(content, delimiter)
                valid_items = [i for i in items if i.strip() != '']

                if len(valid_items) != size:
                    return {'is_valid': False, 'error': f"L{line_number}: Array size mismatch. Declared {size}, found {len(valid_items)} inline items."}
            else:
                # Block Array start
                if REGEX['root_array'].match(trimmed_line) and len(context_stack) == 1:
                    context_stack[0]['type'] = 'array'
                    context_stack[0]['expected'] = size
                    context_stack[0]['count'] = 0

        # --- State Management (Tabular) ---
        if is_inside_tabular_array:
            root_context = context_stack[0]
            # Check if we are still inside tabular data based on indentation
            # Logic from JS: if (currentIndent >= rootContext.indent || (rootContext.indent === 0 && currentIndent > 0))
            if current_indent >= root_context['indent'] or (root_context['indent'] == 0 and current_indent > 0):
                if ':' in trimmed_line and not trimmed_line.startswith('"'):
                    return {'is_valid': False, 'error': f"L{line_number}: Tabular rows cannot contain a colon."}
                
                if root_context['type'] == 'array':
                    root_context['count'] += 1
                
                if root_context['indent'] == 0:
                    root_context['indent'] = current_indent
                continue
            else:
                is_inside_tabular_array = False

        # --- Indentation Check ---
        if current_indent > required_indent:
            # New Block
            prev_line_trimmed = lines[line_number - 2].strip() if line_number >= 2 else ''
            if not opens_new_block(prev_line_trimmed):
                return {'is_valid': False, 'error': f"L{line_number}: Indentation error."}

            new_context = {'indent': current_indent, 'type': 'object'}

            prev_array_match = REGEX['array_key'].match(prev_line_trimmed) or REGEX['root_array'].match(prev_line_trimmed)
            if prev_array_match:
                is_root_array_already_set = (REGEX['root_array'].match(prev_line_trimmed) and
                                           len(context_stack) == 1 and
                                           context_stack[0]['type'] == 'array')

                if not is_root_array_already_set:
                    size = int(prev_array_match.group(1))
                    new_context = {'indent': current_indent, 'type': 'array', 'expected': size, 'count': 0}
                    context_stack.append(new_context)
            else:
                context_stack.append(new_context)

            if len(context_stack) == 1 and context_stack[0]['type'] == 'array' and context_stack[0]['indent'] == 0:
                context_stack[0]['indent'] = current_indent

            target_context = context_stack[-1]
            if target_context['type'] == 'array':
                if REGEX['list_item'].match(trimmed_line):
                    target_context['count'] += 1

        elif current_indent < required_indent:
            # Un-indentation
            found_match = False

            while len(context_stack) > 1:
                popped = context_stack.pop()

                if popped['type'] == 'array':
                    if popped['count'] != popped['expected']:
                        return {'is_valid': False, 'error': f"Array size mismatch. Declared {popped['expected']}, found {popped['count']} items (ending around L{line_number})."}

                if current_indent == context_stack[-1]['indent']:
                    found_match = True
                    break

            if not found_match and current_indent != 0:
                return {'is_valid': False, 'error': f"L{line_number}: Invalid un-indentation."}

            parent_context = context_stack[-1]
            if parent_context['type'] == 'array':
                if REGEX['list_item'].match(trimmed_line):
                    parent_context['count'] += 1

        else:
            # Same Indent
            current_context = context_stack[-1]
            if current_context['type'] == 'array':
                if REGEX['list_item'].match(trimmed_line):
                    current_context['count'] += 1

        # --- Syntax Check ---
        if REGEX['array_key'].match(trimmed_line) or REGEX['root_array'].match(trimmed_line):
            if starts_tabular(trimmed_line):
                is_inside_tabular_array = True
        elif REGEX['map_key'].match(trimmed_line):
            pass
        elif REGEX['list_item'].match(trimmed_line):
            pass
        elif ':' in trimmed_line:
            if not REGEX['key_value'].match(trimmed_line):
                return {'is_valid': False, 'error': f"L{line_number}: Invalid Key-Value assignment."}
        elif trimmed_line.startswith('"') and trimmed_line.endswith('"'):
            pass
        else:
            return {'is_valid': False, 'error': f"L{line_number}: Unrecognized TOON syntax."}

    # Final check
    while len(context_stack) > 1:
        popped = context_stack.pop()
        if popped['type'] == 'array':
            if popped['count'] != popped['expected']:
                return {'is_valid': False, 'error': f"Array size mismatch. Declared {popped['expected']}, found {popped['count']} items."}

    # Check root array if applicable
    if context_stack[0]['type'] == 'array':
        if context_stack[0]['count'] != context_stack[0]['expected']:
            return {'is_valid': False, 'error': f"Root Array size mismatch. Declared {context_stack[0]['expected']}, found {context_stack[0]['count']} items."}

    return {'is_valid': True, 'error': None}
