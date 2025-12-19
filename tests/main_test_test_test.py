```python
import builtins
import runpy
from pathlib import Path
from unittest import mock

import pytest


@pytest.fixture
def mock_path_home(monkeypatch):
    fake_home = Path("/tmp/fake_home")
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    return fake_home


@pytest.fixture
def mock_organize_folder(monkeypatch):
    with mock.patch("src.organizer.organize_folder") as m:
        yield m


@pytest.fixture
def mock_display_results(monkeypatch):
    with mock.patch("src.ui.fancy_ui.display_results") as m:
        yield m


@pytest.fixture
def mock_print(monkeypatch):
    with mock.patch.object(builtins, "print") as m:
        yield m


def test_main_exec_calls_functions(
    mock_path_home,
    mock_organize_folder,
    mock_display_results,
    mock_print,
):
    """Verify that main imports and calls the expected functions with correct arguments."""
    expected_path = mock_path_home / "Downloads"
    moved_files_stub = {"txt": ["a.txt"], "images": ["b.png"]}

    mock_organize_folder.return_value = moved_files_stub

    runpy.run_path("scripts/folder-organizer/main.py", run_name="__main__")

    mock_organize_folder.assert_called_once_with(expected_path)
    mock_display_results.assert_called_once_with(moved_files_stub)
    mock_print.assert_called_once_with(moved_files_stub)


def test_main_propagates_organize_exception(
    mock_path_home,
    mock_display_results,
    mock_print,
):
    """If organize_folder raises, the exception should bubble up and no further calls occur."""
    with mock.patch(
        "src.organizer.organize_folder",
        side_effect=RuntimeError("organize error"),
    ):
        with pytest.raises(RuntimeError, match="organize error"):
            runpy.run_path("scripts/folder-organizer/main.py", run_name="__main__")

    mock_display_results.assert_not_called()
    mock_print.assert_not_called()


def test_main_handles_empty_result(
    mock_path_home,
    mock_organize_folder,
    mock_display_results,
    mock_print,
):
    """When organize_folder returns an empty dict, display_results and print should receive it."""
    expected_path = mock_path_home / "Downloads"
    mock_organize_folder.return_value = {}

    runpy.run_path("scripts/folder-organizer/main.py", run_name="__main__")

    mock_organize_folder.assert_called_once_with(expected_path)
    mock_display_results.assert_called_once_with({})
    mock_print.assert_called_once_with({})


def test_main_propagates_display_exception(
    mock_path_home,
    mock_organize_folder,
    mock_display_results,
    mock_print,
):
    """If display_results raises, the exception propagates and print is not executed."""
    moved_files_stub = {"doc": ["c.docx"]}
    mock_organize_folder.return_value = moved_files_stub
    mock_display_results.side_effect = ValueError("display error")

    with pytest.raises(ValueError, match="display error"):
        runpy.run_path("scripts/folder-organizer/main.py", run_name="__main__")

    mock_organize_folder.assert_called_once()
    mock_display_results.assert_called_once_with(moved_files_stub)
    mock_print.assert_not_called()


def test_main_uses_downloads_subdirectory(
    mock_path_home,
    mock_organize_folder,
    mock_display_results,
    mock_print,
):
    """Ensure the script always targets the 'Downloads' subdirectory of the home path."""
    # Arrange a different fake home to verify path concatenation
    alternative_home = Path("/var/tmp/alt_home")
    mock_path_home = alternative_home
    # Monkeypatch Path.home to return the alternative path for this test only
    with mock.patch.object(Path, "home", return_value=alternative_home):
        mock_organize_folder.return_value = {"misc": []}
        runpy.run_path("scripts/folder-organizer/main.py", run_name="__main__")

    expected_path = alternative_home / "Downloads"
    mock_organize_folder.assert_called_once_with(expected_path)
    mock_display_results.assert_called_once()
    mock_print.assert_called_once()


def test_main_exec_with_multiple_file_types(
    mock_path_home,
    mock_organize_folder,
    mock_display_results,
    mock_print,
):
    """Verify that main handles a scenario with multiple file types."""
    expected_path = mock_path_home / "Downloads"
    moved_files_stub = {
        "txt": ["a.txt", "b.txt"],
        "images": ["c.png", "d.jpg"],
        "videos": ["e.mp4"],
    }

    mock_organize_folder.return_value = moved_files_stub

    runpy.run_path("scripts/folder-organizer/main.py", run_name="__main__")

    mock_organize_folder.assert_called_once_with(expected_path)
    mock_display_results.assert_called_once_with(moved_files_stub)
    mock_print.assert_called_once_with(moved_files_stub)


def test_main_exec_with_no_files(
    mock_path_home,
    mock_organize_folder,
    mock_display_results,
    mock_print,
):
    """Verify that main handles a scenario with no files to organize."""
    expected_path = mock_path_home / "Downloads"
    mock_organize_folder.return_value = {}

    runpy.run_path("scripts/folder-organizer/main.py", run_name="__main__")

    mock_organize_folder.assert_called_once_with(expected_path)
    mock_display_results.assert_called_once_with({})
    mock_print.assert_called_once_with({}) 


def test_main_exec_with_empty_file_list(
    mock_path_home,
    mock_organize_folder,
    mock_display_results,
    mock_print,
):
    """Verify that main handles a scenario with an empty file list for a specific file type."""
    expected_path = mock_path_home / "Downloads"
    moved_files_stub = {"txt": [], "images": ["a.png"]}

    mock_organize_folder.return_value = moved_files_stub

    runpy.run_path("scripts/folder-organizer/main.py", run_name="__main__")

    mock_organize_folder.assert_called_once_with(expected_path)
    mock_display_results.assert_called_once_with(moved_files_stub)
    mock_print.assert_called_once_with(moved_files_stub)
```