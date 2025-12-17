import csv, json, io
from ..utils import extract_csv_from_string, extract_json_from_string, flatten_json, unflatten_object


def csv_to_json(csv_string):
    """
    Converts CSV to JSON format.
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

            json_string = json.dumps(parsed_data)
            json_output = json_string.strip()
            converted_text = converted_text.replace(csv_block, json_output)
            iteration_count += 1
        except:
            raise Exception('Error while converting CSV to JSON')

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

def json_to_csv(data):
    """
    Converts JSON to CSV format.
    """
    if not data: raise ValueError("Input must be a non-empty")
    
    # Handle non-string input
    if not isinstance(data, str): data = json.dumps(data)

    converted_text = data
    iteration_count = 0
    max_iterations = 100

    while iteration_count < max_iterations:
        json_block = extract_json_from_string(converted_text)
        if not json_block: break
        
        try:
            json_data = json.loads(json_block)
            
            if not isinstance(json_data, list): raise ValueError(
                "JSON data must be an array of objects to convert to CSV"
            )

            # Flatten the JSON data
            flat_json_data = flatten_json(json_data)

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

            csv_output = output.getvalue().strip()
            converted_text = converted_text.replace(json_block, csv_output)
            iteration_count += 1
        except:
            raise Exception('Error while converting JSON to CSV')
        
    return converted_text
