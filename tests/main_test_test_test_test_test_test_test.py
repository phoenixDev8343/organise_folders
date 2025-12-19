```python
import builtins
import sys
import types
from pathlib import Path
from unittest import mock

import pytest
import runpy


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
    Patch src.organizer.organize_folder to a mock that returns a predictable dict.
    """
    with mock.patch("src.organizer.organize_folder") as mock_func:
        mock_func.return_value = {"txt": ["file1.txt"], "pdf": ["doc1.pdf"]}
        yield mock_func


@pytest.fixture
def mock_display_results():
    """
    Patch src.ui.fancy_ui.display_results to a mock function.
    """
    with mock.patch("src.ui.fancy_ui.display_results") as mock_func:
        yield mock_func


def test_main_execution_calls_functions_and_prints(
    mock_path_home, mock_organize_folder, mock_display_results, capsys
):
    """
    Verify that when the module is executed as a script:
    - Path.home() is used to build the downloads directory.
    - organize_folder is called with the correct Path.
    - display_results is called with the result of organize_folder.
    - The returned dict is printed.
    """
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    expected_downloads = mock_path_home / "Downloads"
    mock_organize_folder.assert_called_once_with(expected_downloads)

    mock_display_results.assert_called_once_with(
        {"txt": ["file1.txt"], "pdf": ["doc1.pdf"]}
    )

    captured = capsys.readouterr()
    assert captured.out.strip() == str({"txt": ["file1.txt"], "pdf": ["doc1.pdf"]})


def test_main_handles_organize_folder_exception(
    mock_path_home, mock_display_results, capsys
):
    """
    Simulate organize_folder raising an exception and ensure it propagates.
    """
    with mock.patch(
        "src.organizer.organize_folder", side_effect=RuntimeError("organizer error")
    ):
        with pytest.raises(RuntimeError, match="organizer error"):
            runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    mock_display_results.assert_not_called()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_main_prints_empty_dict_when_no_files_moved(
    mock_path_home, mock_display_results
):
    """
    When organize_folder returns an empty dict, ensure the printed output reflects it.
    """
    with mock.patch(
        "src.organizer.organize_folder", return_value={}
    ) as mock_organize:
        with mock.patch.object(builtins, "print") as mock_print:
            runpy.run_module("scripts.folder-organizer.main", run_name="__main__")
            mock_organize.assert_called_once()
            mock_display_results.assert_called_once_with({})
            mock_print.assert_called_once_with("{}")


def test_main_path_home_is_called_once(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify that Path.home() is called only once.
    """
    with mock.patch.object(Path, "home") as mock_path_home_func:
        runpy.run_module("scripts.folder-organizer.main", run_name="__main__")
        mock_path_home_func.assert_called_once()


def test_main_organize_folder_is_called_once(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify that organize_folder is called only once.
    """
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")
    mock_organize_folder.assert_called_once()


def test_main_display_results_is_called_once(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify that display_results is called only once.
    """
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")
    mock_display_results.assert_called_once()


def test_main_handles_empty_downloads_folder(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Simulate an empty downloads folder and ensure it is handled correctly.
    """
    mock_organize_folder.return_value = {}
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")
    mock_organize_folder.assert_called_once()
    mock_display_results.assert_called_once_with({})
    captured = capsys.readouterr()
    assert captured.out.strip() == str({})


def test_main_handles_no_files_to_move(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Simulate no files to move and ensure it is handled correctly.
    """
    mock_organize_folder.return_value = {}
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")
    mock_organize_folder.assert_called_once()
    mock_display_results.assert_called_once_with({})
    captured = capsys.readouterr()
    assert captured.out.strip() == str({}) 


def test_main_execution_with_multiple_file_types(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify that when the module is executed as a script with multiple file types:
    - organize_folder is called with the correct Path.
    - display_results is called with the result of organize_folder.
    - The returned dict is printed.
    """
    mock_organize_folder.return_value = {"txt": ["file1.txt", "file2.txt"], "pdf": ["doc1.pdf", "doc2.pdf"]}
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")
    expected_downloads = mock_path_home / "Downloads"
    mock_organize_folder.assert_called_once_with(expected_downloads)
    mock_display_results.assert_called_once_with(
        {"txt": ["file1.txt", "file2.txt"], "pdf": ["doc1.pdf", "doc2.pdf"]}
    )
    captured = capsys.readouterr()
    assert captured.out.strip() == str({"txt": ["file1.txt", "file2.txt"], "pdf": ["doc1.pdf", "doc2.pdf"]})

def test_main_execution_with_no_file_types(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify that when the module is executed as a script with no file types:
    - organize_folder is called with the correct Path.
    - display_results is called with the result of organize_folder.
    - The returned dict is printed.
    """
    mock_organize_folder.return_value = {}
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")
    expected_downloads = mock_path_home / "Downloads"
    mock_organize_folder.assert_called_once_with(expected_downloads)
    mock_display_results.assert_called_once_with({})
    captured = capsys.readouterr()
    assert captured.out.strip() == str({})

def test_main_execution_with_single_file_type(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify that when the module is executed as a script with a single file type:
    - organize_folder is called with the correct Path.
    - display_results is called with the result of organize_folder.
    - The returned dict is printed.
    """
    mock_organize_folder.return_value = {"txt": ["file1.txt"]}
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")
    expected_downloads = mock_path_home / "Downloads"
    mock_organize_folder.assert_called_once_with(expected_downloads)
    mock_display_results.assert_called_once_with(
        {"txt": ["file1.txt"]}
    )
    captured = capsys.readouterr()
    assert captured.out.strip() == str({"txt": ["file1.txt"]})

def test_main_execution_with_invalid_file_types(mock_path_home, mock_organize_folder, mock_display_results, capsys):
    """
    Verify that when the module is executed as a script with invalid file types:
    - organize_folder is called with the correct Path.
    - display_results is called with the result of organize_folder.
    - The returned dict is printed.
    """
    mock_organize_folder.return_value = {"invalid": ["file1.invalid"]}
    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")
    expected_downloads = mock_path_home / "Downloads"
    mock_organize_folder.assert_called_once_with(expected_downloads)
    mock_display_results.assert_called_once_with(
        {"invalid": ["file1.invalid"]}
    )
    captured = capsys.readouterr()
    assert captured.out.strip() == str({"invalid": ["file1.invalid"]})
```