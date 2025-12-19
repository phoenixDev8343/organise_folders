import builtins
import sys
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
    # Arrange
    expected_path = mock_path_home / "Downloads"
    moved_files_stub = {"txt": ["a.txt"], "images": ["b.png"]}
    mock_organize_folder.return_value = moved_files_stub

    # Act
    runpy.run_path("scripts/folder-organizer/main.py", run_name="__main__")

    # Assert
    mock_organize_folder.assert_called_once_with(expected_path)
    mock_display_results.assert_called_once_with(moved_files_stub)
    mock_print.assert_called_once_with(moved_files_stub)


def test_main_propagates_organize_exception(
    mock_path_home,
    mock_display_results,
    mock_print,
):
    # Arrange
    with mock.patch("src.organizer.organize_folder", side_effect=RuntimeError("organize error")):
        # Act & Assert
        with pytest.raises(RuntimeError, match="organize error"):
            runpy.run_path("scripts/folder-organizer/main.py", run_name="__main__")

    # Ensure display_results and print were never called
    mock_display_results.assert_not_called()
    mock_print.assert_not_called()