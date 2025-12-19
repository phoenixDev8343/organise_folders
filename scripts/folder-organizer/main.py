# main.py

from pathlib import Path
from src.organizer  import organize_folder
from src.ui.fancy_ui import display_results

if __name__ == "__main__":
    downloads_dir = Path.home() / "Downloads"   # Get the user's Downloads folder
    moved_files = organize_folder(downloads_dir)    # Organize files in Downloads
    display_results(moved_files)    # Display results in categorized format
