import importlib.util
import runpy
import sys
from pathlib import Path
import types

import pytest


def load_module_without_main():
    """
    Load the folder-organizer main script as a module without triggering its
    ``if __name__ == "__main__"`` block.
    """
    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"
    spec = importlib.util.spec_from_file_location("folder_organizer_main", script_path)
    module = importlib.util.module_from_spec(spec)
    module.__name__ = "folder_organizer_main"
    sys.modules["folder_organizer_main"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(autouse=True)
def clean_sys_modules():
    """
    Ensure that any monkeypatched modules are removed after each test to avoid
    cross‑test contamination.
    """
    original_modules = sys.modules.copy()
    yield
    sys.modules.clear()
    sys.modules.update(original_modules)


def test_import_does_not_execute_main_block(monkeypatch):
    """
    Verify that importing the script does not execute the ``__main__`` block.
    """
    called = {"organize": False, "display": False}

    def fake_organize_folder(_):
        called["organize"] = True
        return {}

    def fake_display_results(_):
        called["display"] = True

    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))
    monkeypatch.setitem(sys.modules, "src.ui.fancy_ui", types.SimpleNamespace(display_results=fake_display_results))

    load_module_without_main()

    assert not called["organize"]
    assert not called["display"]


def test_main_executes_functions_and_prints_output(monkeypatch, capsys):
    """
    When executed as ``__main__``, the script should:
    1. Call ``organize_folder`` with the user's Downloads directory.
    2. Pass the result to ``display_results``.
    3. Print the result to stdout.
    """
    fake_home = Path("/fake/home")
    expected_downloads = fake_home / "Downloads"

    recorded = {"organize_arg": None, "display_arg": None}

    def fake_organize_folder(path):
        recorded["organize_arg"] = path
        return {"txt": 5, "pdf": 2}

    def fake_display_results(result):
        recorded["display_arg"] = result

    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))
    monkeypatch.setitem(sys.modules, "src.ui.fancy_ui", types.SimpleNamespace(display_results=fake_display_results))

    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"
    runpy.run_path(str(script_path), run_name="__main__")

    assert recorded["organize_arg"] == expected_downloads
    assert recorded["display_arg"] == {"txt": 5, "pdf": 2}
    captured = capsys.readouterr()
    assert str({"txt": 5, "pdf": 2}) in captured.out


def test_main_handles_empty_result(monkeypatch, capsys):
    """
    Ensure the script behaves correctly when ``organize_folder`` returns an empty dict.
    """
    fake_home = Path("/home/user")
    expected_downloads = fake_home / "Downloads"

    recorded = {"organize_arg": None, "display_arg": None}

    def fake_organize_folder(path):
        recorded["organize_arg"] = path
        return {}

    def fake_display_results(result):
        recorded["display_arg"] = result

    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))
    monkeypatch.setitem(sys.modules, "src.ui.fancy_ui", types.SimpleNamespace(display_results=fake_display_results))

    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"
    runpy.run_path(str(script_path), run_name="__main__")

    assert recorded["organize_arg"] == expected_downloads
    assert recorded["display_arg"] == {}
    captured = capsys.readouterr()
    assert str({}) in captured.out


def test_main_propagates_organize_exception(monkeypatch):
    """
    If ``organize_folder`` raises an exception, the script should not swallow it.
    """
    class DummyError(RuntimeError):
        pass

    def fake_organize_folder(_):
        raise DummyError("organizer failure")

    def fake_display_results(_):
        # Should never be called
        pytest.fail("display_results should not be invoked when organize_folder fails")

    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))
    monkeypatch.setitem(sys.modules, "src.ui.fancy_ui", types.SimpleNamespace(display_results=fake_display_results))

    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"

    with pytest.raises(DummyError):
        runpy.run_path(str(script_path), run_name="__main__")


def test_main_continues_when_display_raises(monkeypatch, capsys):
    """
    ``display_results`` errors should not prevent the result from being printed.
    """
    fake_home = Path("/home/guest")
    expected_downloads = fake_home / "Downloads"

    recorded = {"organize_arg": None, "display_called": False}

    def fake_organize_folder(path):
        recorded["organize_arg"] = path
        return {"img": 3}

    def fake_display_results(_):
        recorded["display_called"] = True
        raise ValueError("UI failure")

    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))
    monkeypatch.setitem(sys.modules, "src.ui.fancy_ui", types.SimpleNamespace(display_results=fake_display_results))

    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"

    # The script is expected to let the exception propagate; if the original script
    # catches it internally, this test will still succeed because the printed output
    # is verified.
    try:
        runpy.run_path(str(script_path), run_name="__main__")
    except Exception:
        pass

    assert recorded["organize_arg"] == expected_downloads
    assert recorded["display_called"]
    captured = capsys.readouterr()
    assert str({"img": 3}) in captured.out