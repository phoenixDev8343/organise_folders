```python
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
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    expected_downloads = fake_home / "Downloads"
    mock_organize.assert_called_once_with(expected_downloads)
    mock_display.assert_called_once_with(mock_organize.return_value)

    captured = capsys.readouterr()
    assert str(mock_organize.return_value) in captured.out


def test_main_handles_exception(fake_home, mock_display):
    """
    Ensure that if organize_folder raises an exception, the script propagates it
    and does not call display_results.
    """
    with mock.patch(
        "src.organizer.organize_folder",
        side_effect=RuntimeError("organizer error")
    ) as mock_organize:
        with pytest.raises(RuntimeError, match="organizer error"):
            runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

        mock_display.assert_not_called()
        mock_organize.assert_called_once_with(fake_home / "Downloads")


def test_main_with_empty_result(fake_home, mock_display):
    """
    Verify behavior when organize_folder returns an empty dictionary.
    The script should still print the empty dict and call display_results.
    """
    with mock.patch(
        "src.organizer.organize_folder",
        return_value={}
    ) as mock_organize:
        runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

        mock_organize.assert_called_once_with(fake_home / "Downloads")
        mock_display.assert_called_once_with({})
        # Ensure the printed output reflects the empty result
        captured = capsys.readouterr()
        assert "{}" in captured.out


def test_main_display_raises_propagates(fake_home, mock_organize):
    """
    If display_results raises an exception, it should propagate and the script
    should not suppress it.
    """
    with mock.patch(
        "src.ui.fancy_ui.display_results",
        side_effect=ValueError("display error")
    ) as mock_display:
        with pytest.raises(ValueError, match="display error"):
            runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

        mock_organize.assert_called_once_with(fake_home / "Downloads")
        mock_display.assert_called_once_with(mock_organize.return_value)


def test_main_downloads_path_missing(fake_home, mock_organize, mock_display):
    """
    Simulate a scenario where the Downloads directory does not exist.
    The script should still pass the expected path to organize_folder.
    """
    # Remove the Downloads folder if it was inadvertently created
    downloads_path = fake_home / "Downloads"
    if downloads_path.exists():
        downloads_path.rmdir()

    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    mock_organize.assert_called_once_with(downloads_path)
    mock_display.assert_called_once_with(mock_organize.return_value)


def test_main_stdout_is_string_representation(fake_home, mock_organize, capsys):
    """
    Ensure that the printed output is exactly the string representation of the
    dictionary returned by organize_folder (including ordering).
    """
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")
    captured = capsys.readouterr()
    # The output may contain a newline; strip for comparison
    assert captured.out.strip() == str(mock_organize.return_value)


def test_main_with_custom_path(fake_home, mock_organize, mock_display, capsys):
    """
    Test that the script works with a custom path.
    """
    custom_path = fake_home / "Custom"
    custom_path.mkdir()
    with mock.patch("sys.argv", ["script_name", str(custom_path)]):
        runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    mock_organize.assert_called_once_with(custom_path)
    mock_display.assert_called_once_with(mock_organize.return_value)


def test_main_with_invalid_path(fake_home, mock_organize, mock_display, capsys):
    """
    Test that the script raises an error with an invalid path.
    """
    invalid_path = fake_home / "Invalid"
    with mock.patch("sys.argv", ["script_name", str(invalid_path)]):
        with pytest.raises(FileNotFoundError):
            runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    mock_organize.assert_not_called()
    mock_display.assert_not_called()


def test_main_with_no_args(fake_home, mock_organize, mock_display, capsys):
    """
    Test that the script uses the default path when no arguments are provided.
    """
    with mock.patch("sys.argv", ["script_name"]):
        runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    expected_downloads = fake_home / "Downloads"
    mock_organize.assert_called_once_with(expected_downloads)
    mock_display.assert_called_once_with(mock_organize.return_value)
```