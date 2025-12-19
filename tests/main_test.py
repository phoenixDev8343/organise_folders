import builtins
import io
import sys
import types
from pathlib import Path
from unittest import mock

import pytest
import runpy


@pytest.fixture
def fake_home(tmp_path):
    """
    Fixture that patches Path.home() to return a temporary directory.
    """
    with mock.patch.object(Path, "home", return_value=tmp_path):
        yield tmp_path


@pytest.fixture
def mock_organize():
    """
    Fixture that patches src.organizer.organize_folder and returns a known result.
    """
    with mock.patch("src.organizer.organize_folder") as mocked:
        mocked.return_value = {"Images": ["photo.jpg"], "Docs": ["report.pdf"]}
        yield mocked


@pytest.fixture
def mock_display():
    """
    Fixture that patches src.ui.fancy_ui.display_results.
    """
    with mock.patch("src.ui.fancy_ui.display_results") as mocked:
        yield mocked


def test_main_executes_functions(fake_home, mock_organize, mock_display, capsys):
    """
    Verify that the script's __main__ block:
    - Calls organize_folder with the user's Downloads directory.
    - Calls display_results with the result of organize_folder.
    - Prints the result to stdout.
    """
    # Run the module as a script
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    # Expected path to the Downloads folder
    expected_downloads = fake_home / "Downloads"

    # Assert organize_folder was called once with the correct argument
    mock_organize.assert_called_once_with(expected_downloads)

    # Assert display_results was called once with the result from organize_folder
    mock_display.assert_called_once_with(mock_organize.return_value)

    # Capture printed output and verify it contains the string representation of the moved files
    captured = capsys.readouterr()
    assert str(mock_organize.return_value) in captured.out


def test_main_handles_exception(fake_home, mock_display):
    """
    Ensure that if organize_folder raises an exception, the script propagates it
    and does not call display_results.
    """
    with mock.patch("src.organizer.organize_folder", side_effect=RuntimeError("organizer error")) as mock_organize:
        with pytest.raises(RuntimeError, match="organizer error"):
            runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

        # display_results should never be called
        mock_display.assert_not_called()
        mock_organize.assert_called_once_with(fake_home / "Downloads")