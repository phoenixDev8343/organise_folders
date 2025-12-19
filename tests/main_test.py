import builtins
import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import runpy

# Helper to reload the module under test with fresh state
def reload_main_module(monkeypatch):
    # Ensure the module is removed from sys.modules before reloading
    if "scripts.folder-organizer.main" in sys.modules:
        del sys.modules["scripts.folder-organizer.main"]
    elif "scripts.folder-organizer.main".replace("-", "_") in sys.modules:
        del sys.modules["scripts.folder-organizer.main".replace("-", "_")]
    # Reload the module
    return importlib.import_module("scripts.folder-organizer.main")


def test_main_calls_organize_and_display(monkeypatch, capsys):
    # Arrange
    fake_home = Path("/fake/home")
    fake_downloads = fake_home / "Downloads"
    moved_files_stub = {"txt": ["a.txt"], "pdf": ["b.pdf"]}

    # Mock Path.home to return our fake home directory
    monkeypatch.setattr(Path, "home", lambda: fake_home)

    # Spy objects to capture calls
    called = SimpleNamespace(organize_args=None, display_args=None)

    def fake_organize_folder(path):
        called.organize_args = path
        return moved_files_stub

    def fake_display_results(results):
        called.display_args = results

    monkeypatch.setattr("src.organizer.organize_folder", fake_organize_folder)
    monkeypatch.setattr("src.ui.fancy_ui.display_results", fake_display_results)

    # Act
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    # Assert
    assert called.organize_args == fake_downloads
    assert called.display_args == moved_files_stub

    captured = capsys.readouterr()
    # The script prints the moved_files dict
    assert str(moved_files_stub) in captured.out


def test_main_with_empty_result(monkeypatch, capsys):
    # Arrange
    fake_home = Path("/another/fake/home")
    fake_downloads = fake_home / "Downloads"
    moved_files_stub = {}

    monkeypatch.setattr(Path, "home", lambda: fake_home)

    def fake_organize_folder(path):
        return moved_files_stub

    displayed = {"called": False, "arg": None}

    def fake_display_results(results):
        displayed["called"] = True
        displayed["arg"] = results

    monkeypatch.setattr("src.organizer.organize_folder", fake_organize_folder)
    monkeypatch.setattr("src.ui.fancy_ui.display_results", fake_display_results)

    # Act
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    # Assert
    assert displayed["called"] is True
    assert displayed["arg"] == moved_files_stub

    captured = capsys.readouterr()
    # Should print an empty dict representation
    assert captured.out.strip().endswith("{}")