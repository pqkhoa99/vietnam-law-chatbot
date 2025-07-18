
import json

def read_json_file(file_path):
    """
    Read and parse a JSON file
    Args:
        file_path (str): Path to the JSON file
    Returns:
        dict: Parsed JSON data
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None
    

def save_to_json_file(data, file_path):
    """
    Save data to a JSON file
    Args:
        data: Data to save (dict or list)
        file_path (str): Path where to save the JSON file
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error saving to {file_path}: {str(e)}")
        return False