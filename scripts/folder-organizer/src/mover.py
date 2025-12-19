# src/mover.py

from pathlib import Path
import shutil

# ----- Move a single file into its designated folder -----
def move_file(file_path: Path, target_folder: Path) -> str:
    """
    Move a file to the target folder, creating the folder if missing.
    """
    # Ensure destination folder exists
    target_folder.mkdir(parents=True, exist_ok=True)
    # Move the file
    shutil.move(str(file_path), str(target_folder))
    # Return folder name for tracking
    return target_folder.name
