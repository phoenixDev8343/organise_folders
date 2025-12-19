```python
import builtins
import sys
import runpy
from pathlib import Path
from unittest import mock

import pytest


@pytest.fixture
def mock_path_home(tmp_path):
    """
    Patch Path.home() to return a temporary directory.
    """
    with mock.patch.object(Path, "home", return_value=tmp_path):
        yield tmp_path


@pytest.fixture
def mock_organize_folder():
    """
    Patch src.organizer.organize_folder and provide a mock.
    """
    with mock.patch("src.organizer.organize_folder") as mock_func:
        yield mock_func


@pytest.fixture
def mock_display_results():
    """
    Patch src.ui.fancy_ui.display_results and provide a mock.
    """
    with mock.patch("src.ui.fancy_ui.display_results") as mock_func:
        yield mock_func


def run_main_module():
    """
    Execute the main module as if it were run as a script.
    """
    # Ensure the module is executed with __name__ == "__main__"
    return runpy.run_module("scripts.folder-organizer.main", run_name="__main__")


def test_main_successful_organization(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify that the main script calls organize_folder, passes its result to display_results,
    and prints the returned mapping.
    """
    expected_result = {"Images": ["photo.jpg"], "Docs": ["file.pdf"]}

    mock_organize_folder.return_value = expected_result

    # Run the script
    run_main_module()

    # Assertions
    mock_organize_folder.assert_called_once_with(mock_path_home / "Downloads")
    mock_display_results.assert_called_once_with(expected_result)

    captured = capsys.readouterr()
    # The script prints the dictionary representation
    assert str(expected_result) in captured.out


def test_main_empty_result(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify behavior when organize_folder returns an empty dict.
    """
    expected_result = {}

    mock_organize_folder.return_value = expected_result

    run_main_module()

    mock_organize_folder.assert_called_once_with(mock_path_home / "Downloads")
    mock_display_results.assert_called_once_with(expected_result)

    captured = capsys.readouterr()
    assert str(expected_result) in captured.out


def test_main_organizer_raises_exception(mock_path_home, mock_organize_folder):
    """
    Ensure that exceptions from organize_folder propagate out of the script.
    """
    mock_organize_folder.side_effect = RuntimeError("Organizer failure")

    with pytest.raises(RuntimeError, match="Organizer failure"):
        run_main_module()

    mock_organize_folder.assert_called_once_with(mock_path_home / "Downloads")


def test_main_organizer_returns_none(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify behavior when organize_folder returns None.
    """
    expected_result = None

    mock_organize_folder.return_value = expected_result

    run_main_module()

    mock_organize_folder.assert_called_once_with(mock_path_home / "Downloads")
    mock_display_results.assert_called_once_with(expected_result)

    captured = capsys.readouterr()
    assert str(expected_result) in captured.out


def test_main_organizer_returns_invalid_type(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify behavior when organize_folder returns an invalid type.
    """
    expected_result = [1, 2, 3]

    mock_organize_folder.return_value = expected_result

    run_main_module()

    mock_organize_folder.assert_called_once_with(mock_path_home / "Downloads")
    mock_display_results.assert_called_once_with(expected_result)

    captured = capsys.readouterr()
    assert str(expected_result) in captured.out


def test_main_display_results_raises_exception(mock_path_home, mock_organize_folder, mock_display_results):
    """
    Ensure that exceptions from display_results propagate out of the script.
    """
    mock_organize_folder.return_value = {}
    mock_display_results.side_effect = RuntimeError("Display results failure")

    with pytest.raises(RuntimeError, match="Display results failure"):
        run_main_module()

    mock_organize_folder.assert_called_once_with(mock_path_home / "Downloads")
    mock_display_results.assert_called_once_with({})


def test_main_path_home_raises_exception(mock_path_home, mock_organize_folder):
    """
    Ensure that exceptions from Path.home() propagate out of the script.
    """
    with mock.patch.object(Path, "home", side_effect=RuntimeError("Path home failure")):
        with pytest.raises(RuntimeError, match="Path home failure"):
            run_main_module()

    mock_organize_folder.assert_not_called()


def test_main_run_module_raises_exception():
    """
    Ensure that exceptions from run_module propagate out of the script.
    """
    with mock.patch.object(runpy, "run_module", side_effect=RuntimeError("Run module failure")):
        with pytest.raises(RuntimeError, match="Run module failure"):
            run_main_module()


def test_main_path_home_returns_none(mock_path_home, mock_organize_folder):
    """
    Ensure that the script handles Path.home() returning None.
    """
    with mock.patch.object(Path, "home", return_value=None):
        with pytest.raises(AttributeError):
            run_main_module()

    mock_organize_folder.assert_not_called()


def test_main_organize_folder_returns_empty_list(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify behavior when organize_folder returns an empty list.
    """
    expected_result = []

    mock_organize_folder.return_value = expected_result

    run_main_module()

    mock_organize_folder.assert_called_once_with(mock_path_home / "Downloads")
    mock_display_results.assert_called_once_with(expected_result)

    captured = capsys.readouterr()
    assert str(expected_result) in captured.out


def test_main_organize_folder_returns_tuple(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify behavior when organize_folder returns a tuple.
    """
    expected_result = ("Images", ["photo.jpg"])

    mock_organize_folder.return_value = expected_result

    run_main_module()

    mock_organize_folder.assert_called_once_with(mock_path_home / "Downloads")
    mock_display_results.assert_called_once_with(expected_result)

    captured = capsys.readouterr()
    assert str(expected_result) in captured.out


def test_main_organize_folder_returns_set(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify behavior when organize_folder returns a set.
    """
    expected_result = {"Images", "Docs"}

    mock_organize_folder.return_value = expected_result

    run_main_module()

    mock_organize_folder.assert_called_once_with(mock_path_home / "Downloads")
    mock_display_results.assert_called_once_with(expected_result)

    captured = capsys.readouterr()
    assert str(expected_result) in captured.out
```