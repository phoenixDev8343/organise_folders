# src/ui/ui.py

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

# ----- Display a summary of all moved files, grouped by category -----
def display_results(moved_files):
    """
    Display the moved files in a categorized format.
    
    For each folder, shows folder name and number of files,
    then lists all filenames inside that folder.
    """
    for folder, files in moved_files.items():
        # Header with folder name and file count
        header = Text(f"{folder} ({len(files)} files):", style="bold cyan")
        # Prepare file list as bullet points
        file_list = "\n".join(f" - {f}" for f in files)
        # Wrap in a panel with green border
        panel = Panel(file_list, title=header, expand=False, border_style="green")
        # Print the panel
        console.print(panel)
