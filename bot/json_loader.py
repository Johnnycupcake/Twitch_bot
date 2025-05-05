import json
import logging

def load_json(filename, default=None):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning(f"{filename} not found, using default.")
        return default or {}
    except Exception as e:
        logging.error(f"Error loading {filename}: {e}")
        return default or {}

def save_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Saved data to {filename}")
    except Exception as e:
        logging.error(f"Error saving {filename}: {e}")
