import csv, io
from .json_converter import json_to_toon, toon_to_json
from .utils import extract_csv_from_string, flatten_json, unflatten_object


def csv_to_toon(csv_string):
    """
    Converts CSV to TOON format.
    """
    if not csv_string or not isinstance(csv_string, str):
        raise ValueError("Input must be a non-empty string")
    
    converted_text = csv_string
    iteration_count = 0
    max_iterations = 100

    while iteration_count < max_iterations:
        csv_block = extract_csv_from_string(converted_text)
        if not csv_block: break

        try:
            f = io.StringIO(csv_block)
            reader = csv.DictReader(f)
            data = list(reader)
            
            # Convert values to numbers/booleans/nulls if possible?
            parsed_data = []
            for row in data:
                new_row = {}
                for k, v in row.items():
                    new_row[k] = _infer_type(v)
                parsed_data.append(unflatten_object(new_row))

            toon_string = json_to_toon(parsed_data)
            toon_output = toon_string.strip()
            converted_text = converted_text.replace(csv_block, toon_output)
            iteration_count += 1
        except:
            raise Exception('Error while converting CSV to TOON')

    return converted_text

def _infer_type(val):
    if val is None: return None
    val = val.strip()
    if val == 'true': return True
    if val == 'false': return False
    if val == 'null': return None
    if val == '': return ""
    
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        return val

def toon_to_csv(toon_string):
    """
    Converts TOON to CSV format.
    """
    if not toon_string or not isinstance(toon_string, str):
        raise ValueError("Input must be a non-empty string")
    
    data = toon_to_json(toon_string)
    
    if not isinstance(data, list):
        raise ValueError("TOON data must be an array of objects to convert to CSV")
    
    if not data:
        return ""
    
    # Flatten the JSON data
    flat_json_data = flatten_json(data)
    
    # Collect all keys
    keys = set()
    for item in flat_json_data:
        if isinstance(item, dict):
            keys.update(item.keys())
    
    fieldnames = sorted(list(keys)) # Sort for consistency
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in flat_json_data:
        if isinstance(row, dict):
            writer.writerow(row)
            
    return output.getvalue().strip()
