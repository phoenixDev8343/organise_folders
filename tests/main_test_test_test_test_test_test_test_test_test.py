```python
import runpy
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def temp_home_dir():
    """Create a temporary directory to act as the user's home directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(Path, "home", return_value=Path(tmpdir)):
            yield Path(tmpdir)


def _run_main_module():
    """Helper to execute the main module as a script."""
    # Adjust the module path if the package uses an underscore instead of a hyphen.
    return runpy.run_module("scripts.folder_organizer.main", run_name="__main__")


def test_main_execution_calls_organizer_and_ui(temp_home_dir, capsys):
    """Verify that the script calls organize_folder and display_results with correct arguments and prints the returned value."""
    dummy_result = {"txt": ["file1.txt", "file2.txt"], "images": ["photo.png"]}

    mock_organize = MagicMock(return_value=dummy_result)
    mock_display = MagicMock()

    with patch("src.organizer.organize_folder", mock_organize), \
         patch("src.ui.fancy_ui.display_results", mock_display):
        _run_main_module()

    expected_downloads = temp_home_dir / "Downloads"
    mock_organize.assert_called_once_with(expected_downloads)
    mock_display.assert_called_once_with(dummy_result)

    captured = capsys.readouterr()
    assert captured.out.strip() == str(dummy_result)


def test_main_execution_with_empty_result(temp_home_dir, capsys):
    """Ensure the script works correctly when organize_folder returns an empty dictionary."""
    empty_result = {}

    mock_organize = MagicMock(return_value=empty_result)
    mock_display = MagicMock()

    with patch("src.organizer.organize_folder", mock_organize), \
         patch("src.ui.fancy_ui.display_results", mock_display):
        _run_main_module()

    expected_downloads = temp_home_dir / "Downloads"
    mock_organize.assert_called_once_with(expected_downloads)
    mock_display.assert_called_once_with(empty_result)

    captured = capsys.readouterr()
    assert captured.out.strip() == str(empty_result)


def test_main_raises_when_organizer_fails(temp_home_dir):
    """If organize_folder raises an exception, the script should propagate it."""
    mock_organize = MagicMock(side_effect=RuntimeError("organizer failure"))
    mock_display = MagicMock()

    with patch("src.organizer.organize_folder", mock_organize), \
         patch("src.ui.fancy_ui.display_results", mock_display):
        with pytest.raises(RuntimeError, match="organizer failure"):
            _run_main_module()

    mock_display.assert_not_called()


def test_main_propagates_display_error(temp_home_dir):
    """If display_results raises an exception, the script should propagate it after calling organize_folder."""
    dummy_result = {"doc": ["a.docx"]}

    mock_organize = MagicMock(return_value=dummy_result)
    mock_display = MagicMock(side_effect=ValueError("display failure"))

    with patch("src.organizer.organize_folder", mock_organize), \
         patch("src.ui.fancy_ui.display_results", mock_display):
        with pytest.raises(ValueError, match="display failure"):
            _run_main_module()

    expected_downloads = Path.home() / "Downloads"
    mock_organize.assert_called_once_with(expected_downloads)
    mock_display.assert_called_once_with(dummy_result)


def test_main_does_not_execute_on_import():
    """Importing the module should not trigger the script logic (guarded by if __name__ == '__main__')."""
    with patch("src.organizer.organize_folder") as mock_organize, \
         patch("src.ui.fancy_ui.display_results") as mock_display, \
         patch("builtins.print") as mock_print:
        module = __import__("scripts.folder_organizer.main", fromlist=["*"])
        mock_organize.assert_not_called()
        mock_display.assert_not_called()
        mock_print.assert_not_called()
        assert getattr(module, "__name__") != "__main__"


def test_main_prints_none_when_organizer_returns_none(temp_home_dir, capsys):
    """If organize_folder returns None, the script should print 'None'."""
    mock_organize = MagicMock(return_value=None)
    mock_display = MagicMock()

    with patch("src.organizer.organize_folder", mock_organize), \
         patch("src.ui.fancy_ui.display_results", mock_display):
        _run_main_module()

    expected_downloads = temp_home_dir / "Downloads"
    mock_organize.assert_called_once_with(expected_downloads)
    mock_display.assert_called_once_with(None)

    captured = capsys.readouterr()
    assert captured.out.strip() == "None"


def test_main_handles_path_home_failure(monkeypatch, capsys):
    """If Path.home() raises an exception, the script should propagate it before calling organizer."""
    def broken_home():
        raise OSError("cannot determine home")

    monkeypatch.setattr(Path, "home", broken_home)

    with patch("src.organizer.organize_folder") as mock_organize, \
         patch("src.ui.fancy_ui.display_results") as mock_display:
        with pytest.raises(OSError, match="cannot determine home"):
            _run_main_module()

    mock_organize.assert_not_called()
    mock_display.assert_not_called()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_main_with_unexpected_result_type(temp_home_dir, capsys):
    """If organize_folder returns a non-dict (e.g., list), the script should still print its string representation."""
    unexpected_result = ["file1.txt", "file2.txt"]
    mock_organize = MagicMock(return_value=unexpected_result)
    mock_display = MagicMock()

    with patch("src.organizer.organize_folder", mock_organize), \
         patch("src.ui.fancy_ui.display_results", mock_display):
        _run_main_module()

    expected_downloads = temp_home_dir / "Downloads"
    mock_organize.assert_called_once_with(expected_downloads)
    mock_display.assert_called_once_with(unexpected_result)

    captured = capsys.readouterr()
    assert captured.out.strip() == str(unexpected_result)


def test_organize_folder_on_non_existent_directory(temp_home_dir, monkeypatch):
    """organize_folder should handle non-existent directories."""
    monkeypatch.setattr(Path, "exists", lambda self: False)
    mock_organize = MagicMock()

    with patch("src.organizer.organize_folder", mock_organize):
        _run_main_module()

    mock_organize.assert_called_once()


def test_organize_folder_on_empty_directory(temp_home_dir, monkeypatch):
    """organize_folder should handle empty directories."""
    mock_organize = MagicMock()

    with patch("src.organizer.organize_folder", mock_organize):
        _run_main_module()

    mock_organize.assert_called_once()


def test_display_results_on_empty_result(temp_home_dir, capsys):
    """display_results should handle empty results."""
    empty_result = {}

    mock_display = MagicMock()

    with patch("src.ui.fancy_ui.display_results", mock_display):
        _run_main_module()

    mock_display.assert_called_once_with(empty_result)


def test_display_results_on_non_dict_result(temp_home_dir, capsys):
    """display_results should handle non-dict results."""
    unexpected_result = ["file1.txt", "file2.txt"]

    mock_display = MagicMock()

    with patch("src.ui.fancy_ui.display_results", mock_display):
        _run_main_module()

    mock_display.assert_called_once_with(unexpected_result)


def test_runpy_main_module(temp_home_dir, capsys):
    """runpy should execute the main module."""
    _run_main_module()
    captured = capsys.readouterr()
    assert captured.out != ""


def test_path_home(temp_home_dir):
    """Path.home should return the temporary home directory."""
    assert Path.home() == temp_home_dir


def test_patch_object(temp_home_dir, monkeypatch):
    """patch.object should patch the Path.home method."""
    def mock_home():
        return Path(temp_home_dir)

    monkeypatch.setattr(Path, "home", mock_home)
    assert Path.home() == temp_home_dir
```