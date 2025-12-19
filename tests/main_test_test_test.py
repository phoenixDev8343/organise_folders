import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import runpy


def _clear_main_module():
    """
    Remove the main module from sys.modules to ensure a fresh import.
    Handles both hyphenated and underscore module names.
    """
    module_names = [
        "scripts.folder-organizer.main",
        "scripts.folder_organizer.main",
    ]
    for name in module_names:
        if name in sys.modules:
            del sys.modules[name]


@pytest.fixture(autouse=True)
def reload_main_before_test(monkeypatch):
    """
    Ensure the main module is reloaded with a clean state before each test.
    """
    _clear_main_module()
    yield
    _clear_main_module()


def test_main_calls_organize_and_display(monkeypatch, capsys):
    fake_home = Path("/fake/home")
    fake_downloads = fake_home / "Downloads"
    moved_files_stub = {"txt": ["a.txt"], "pdf": ["b.pdf"]}

    monkeypatch.setattr(Path, "home", lambda: fake_home)

    called = SimpleNamespace(organize_args=None, display_args=None)

    def fake_organize_folder(path):
        called.organize_args = path
        return moved_files_stub

    def fake_display_results(results):
        called.display_args = results

    monkeypatch.setattr("src.organizer.organize_folder", fake_organize_folder)
    monkeypatch.setattr("src.ui.fancy_ui.display_results", fake_display_results)

    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    assert called.organize_args == fake_downloads
    assert called.display_args == moved_files_stub

    captured = capsys.readouterr()
    assert str(moved_files_stub) in captured.out


def test_main_with_empty_result(monkeypatch, capsys):
    fake_home = Path("/another/fake/home")
    fake_downloads = fake_home / "Downloads"
    moved_files_stub = {}

    monkeypatch.setattr(Path, "home", lambda: fake_home)

    def fake_organize_folder(path):
        assert path == fake_downloads
        return moved_files_stub

    displayed = {"called": False, "arg": None}

    def fake_display_results(results):
        displayed["called"] = True
        displayed["arg"] = results

    monkeypatch.setattr("src.organizer.organize_folder", fake_organize_folder)
    monkeypatch.setattr("src.ui.fancy_ui.display_results", fake_display_results)

    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    assert displayed["called"] is True
    assert displayed["arg"] == moved_files_stub

    captured = capsys.readouterr()
    assert captured.out.strip().endswith("{}")


def test_main_organize_raises_exception(monkeypatch):
    fake_home = Path("/error/home")
    monkeypatch.setattr(Path, "home", lambda: fake_home)

    class DummyError(RuntimeError):
        pass

    def fake_organize_folder(_):
        raise DummyError("Organize failed")

    monkeypatch.setattr("src.organizer.organize_folder", fake_organize_folder)

    with pytest.raises(DummyError):
        runpy.run_module("scripts.folder-organizer.main", run_name="__main__")


def test_main_display_raises_exception(monkeypatch):
    fake_home = Path("/display/error")
    fake_downloads = fake_home / "Downloads"
    moved_files_stub = {"img": ["pic.jpg"]}

    monkeypatch.setattr(Path, "home", lambda: fake_home)

    def fake_organize_folder(path):
        assert path == fake_downloads
        return moved_files_stub

    class DisplayError(RuntimeError):
        pass

    def fake_display_results(_):
        raise DisplayError("Display failed")

    monkeypatch.setattr("src.organizer.organize_folder", fake_organize_folder)
    monkeypatch.setattr("src.ui.fancy_ui.display_results", fake_display_results)

    with pytest.raises(DisplayError):
        runpy.run_module("scripts.folder-organizer.main", run_name="__main__")


def test_main_organize_returns_none(monkeypatch, capsys):
    fake_home = Path("/none/home")
    fake_downloads = fake_home / "Downloads"

    monkeypatch.setattr(Path, "home", lambda: fake_home)

    def fake_organize_folder(path):
        assert path == fake_downloads
        return None

    displayed = {"called": False, "arg": None}

    def fake_display_results(results):
        displayed["called"] = True
        displayed["arg"] = results

    monkeypatch.setattr("src.organizer.organize_folder", fake_organize_folder)
    monkeypatch.setattr("src.ui.fancy_ui.display_results", fake_display_results)

    runpy.run_module("scripts.folder-organizer.main", run_name="__main__")

    assert displayed["called"] is True
    assert displayed["arg"] is None

    captured = capsys.readouterr()
    assert "None" in captured.out


def test_main_path_home_raises(monkeypatch):
    class HomeError(RuntimeError):
        pass

    monkeypatch.setattr(Path, "home", lambda: (_ for _ in ()).throw(HomeError("home error")))

    with pytest.raises(HomeError):
        runpy.run_module("scripts.folder-organizer.main", run_name="__main__")