import json
import logging
import os

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

def save_tokens(tokens):
    filename = os.path.join('config','saved_tokens.json')
    with open(filename, "w") as f:
        json.dump(tokens, f)
    print("💾 Tokens saved!")


def load_tokens():
    filename = os.path.join('config', 'saved_tokens.json')
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    else:
        return None