import os
import sys
import json

def resource_path(relative_path):
    """Get absolute path to resource, works for development and PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def load_config(path):
    """Load config.json"""
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config