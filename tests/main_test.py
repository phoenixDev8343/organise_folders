import importlib.util
import runpy
import sys
from pathlib import Path
import types

import pytest


# Helper to load the target script as a module without executing the __main__ block
def load_module_without_main():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "folder-organizer" / "main.py"
    spec = importlib.util.spec_from_file_location("folder_organizer_main", script_path)
    module = importlib.util.module_from_spec(spec)
    # Ensure __name__ is not "__main__" so the block does not run
    module.__name__ = "folder_organizer_main"
    sys.modules["folder_organizer_main"] = module
    spec.loader.exec_module(module)
    return module


def test_import_does_not_execute_main_block(monkeypatch):
    """
    Ensure that importing the script does not trigger the execution of the
    __main__ block (i.e., organize_folder and display_results are not called).
    """
    called = {"organize": False, "display": False}

    def fake_organize_folder(_):
        called["organize"] = True
        return {}

    def fake_display_results(_):
        called["display"] = True

    # Patch the imports that the script would resolve if the __main__ block ran
    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))
    monkeypatch.setitem(sys.modules, "src.ui.fancy_ui", types.SimpleNamespace(display_results=fake_display_results))

    # Load the module without executing the __main__ block
    load_module_without_main()

    # Neither function should have been called during import
    assert not called["organize"]
    assert not called["display"]


def test_main_executes_functions_and_prints_output(monkeypatch, capsys):
    """
    Verify that when the script is executed as __main__, it:
    1. Calls organize_folder with the correct Downloads path.
    2. Calls display_results with the result from organize_folder.
    3. Prints the result to stdout.
    """
    # Prepare a fake home directory
    fake_home = Path("/fake/home")
    expected_downloads = fake_home / "Downloads"

    # Record arguments passed to the mocked functions
    recorded = {"organize_arg": None, "display_arg": None}

    def fake_organize_folder(path):
        recorded["organize_arg"] = path
        return {"txt": 5, "pdf": 2}

    def fake_display_results(result):
        recorded["display_arg"] = result

    # Patch Path.home to return the fake home directory
    monkeypatch.setattr(Path, "home", lambda: fake_home)

    # Patch the external functions
    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))
    monkeypatch.setitem(sys.modules, "src.ui.fancy_ui", types.SimpleNamespace(display_results=fake_display_results))

    # Execute the script as if it were run directly
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "folder-organizer" / "main.py"
    runpy.run_path(str(script_path), run_name="__main__")

    # Verify organize_folder was called with the correct path
    assert recorded["organize_arg"] == expected_downloads

    # Verify display_results received the same result returned by organize_folder
    assert recorded["display_arg"] == {"txt": 5, "pdf": 2}

    # Verify the printed output contains the string representation of the result
    captured = capsys.readouterr()
    assert str({"txt": 5, "pdf": 2}) in captured.out