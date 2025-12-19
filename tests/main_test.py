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
        original_home = Path.home
        # Patch Path.home to return the temporary directory
        with patch.object(Path, "home", return_value=Path(tmpdir)):
            yield Path(tmpdir)


def test_main_execution_calls_organizer_and_ui(temp_home_dir, capsys):
    """Verify that the script calls organize_folder and display_results with correct arguments
    and prints the returned value."""
    dummy_result = {"txt": ["file1.txt", "file2.txt"], "images": ["photo.png"]}

    mock_organize = MagicMock(return_value=dummy_result)
    mock_display = MagicMock()

    # Patch the imported functions in the target module
    with patch("src.organizer.organize_folder", mock_organize), \
         patch("src.ui.fancy_ui.display_results", mock_display):
        # Execute the module as a script
        runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    # Expected downloads directory path
    expected_downloads = temp_home_dir / "Downloads"

    # Assert organize_folder was called once with the correct Path
    mock_organize.assert_called_once_with(expected_downloads)

    # Assert display_results was called once with the result from organize_folder
    mock_display.assert_called_once_with(dummy_result)

    # Capture printed output and verify it matches the string representation of dummy_result
    captured = capsys.readouterr()
    assert captured.out.strip() == str(dummy_result)


def test_main_execution_with_empty_result(temp_home_dir, capsys):
    """Ensure the script works correctly when organize_folder returns an empty dictionary."""
    empty_result = {}

    mock_organize = MagicMock(return_value=empty_result)
    mock_display = MagicMock()

    with patch("src.organizer.organize_folder", mock_organize), \
         patch("src.ui.fancy_ui.display_results", mock_display):
        runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

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
            runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    # display_results should never be called if organize_folder fails
    mock_display.assert_not_called()