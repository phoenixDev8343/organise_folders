# src/organizer.py

from pathlib import Path
from collections import defaultdict
from src.mover import move_file
import json

# ----- Load category definitions from a JSON configuration file -----
def load_categories(config_file=None):
    """Load categories and extensions from config.json."""
    if config_file is None:
        config_file = Path(__file__).parent / "json" / "config.json"
    else:
        config_file = Path(config_file)

    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found at: {config_file}")
    
    # Read JSON content
    with open(config_file, encoding="utf-8") as f:
        return json.load(f)


# ----- Organize the files in the given folder based on their extensions -----
def organize_folder(folder_to_sort: Path):
    """
    Organize files in folder by extension.
    
    Returns dict mapping folder names to moved files.
    """
    categories = load_categories()  # Load categories
    # Map each extension to its folder
    ext_to_folder = {ext.lower(): cat["name"] for cat in categories for ext in cat["extensions"]}

    moved_files = defaultdict(list)

    for item in folder_to_sort.iterdir():
        if item.is_file() and not item.name.startswith("."):  # Skip hidden files
            folder_name = ext_to_folder.get(item.suffix.lower(), "Other")  # Default 'Other'
            destination = folder_to_sort / folder_name
            move_file(item, destination)  # Move file
            moved_files[folder_name].append(item.name)  # Track moved files

    return moved_files
