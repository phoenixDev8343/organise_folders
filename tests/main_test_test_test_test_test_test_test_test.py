```python
import pytest
import importlib.util
import runpy
import sys
from pathlib import Path
import types

@pytest.fixture(autouse=True)
def clean_sys_modules():
    original_modules = sys.modules.copy()
    yield
    sys.modules.clear()
    sys.modules.update(original_modules)

def load_module_without_main():
    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"
    spec = importlib.util.spec_from_file_location("folder_organizer_main", script_path)
    module = importlib.util.module_from_spec(spec)
    module.__name__ = "folder_organizer_main"
    sys.modules["folder_organizer_main"] = module
    spec.loader.exec_module(module)
    return module

def test_import_does_not_execute_main_block(monkeypatch):
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
    class DummyError(RuntimeError):
        pass

    def fake_organize_folder(_):
        raise DummyError("organizer failure")

    def fake_display_results(_):
        pytest.fail("display_results should not be invoked when organize_folder fails")

    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))
    monkeypatch.setitem(sys.modules, "src.ui.fancy_ui", types.SimpleNamespace(display_results=fake_display_results))

    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"

    with pytest.raises(DummyError):
        runpy.run_path(str(script_path), run_name="__main__")

def test_main_continues_when_display_raises(monkeypatch, capsys):
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

    try:
        runpy.run_path(str(script_path), run_name="__main__")
    except Exception:
        pass

    assert recorded["organize_arg"] == expected_downloads
    assert recorded["display_called"]
    captured = capsys.readouterr()
    assert str({"img": 3}) in captured.out

def test_main_prints_non_dict_result(monkeypatch, capsys):
    fake_home = Path("/tmp/home")
    expected_downloads = fake_home / "Downloads"

    recorded = {"organize_arg": None}

    def fake_organize_folder(path):
        recorded["organize_arg"] = path
        return ["file1.txt", "file2.pdf"]

    def fake_display_results(_):
        pass  # No-op

    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))
    monkeypatch.setitem(sys.modules, "src.ui.fancy_ui", types.SimpleNamespace(display_results=fake_display_results))

    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"
    runpy.run_path(str(script_path), run_name="__main__")

    assert recorded["organize_arg"] == expected_downloads
    captured = capsys.readouterr()
    assert str(["file1.txt", "file2.pdf"]) in captured.out

def test_path_home_called_once(monkeypatch):
    call_counter = {"count": 0}

    def fake_home():
        call_counter["count"] += 1
        return Path("/single/call/home")

    def fake_organize_folder(_):
        return {}

    def fake_display_results(_):
        pass

    monkeypatch.setattr(Path, "home", fake_home)
    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))
    monkeypatch.setitem(sys.modules, "src.ui.fancy_ui", types.SimpleNamespace(display_results=fake_display_results))

    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"
    runpy.run_path(str(script_path), run_name="__main__")

    assert call_counter["count"] == 1

def test_main_respects_missing_ui_module(monkeypatch, capsys):
    fake_home = Path("/no/ui/home")
    expected_downloads = fake_home / "Downloads"

    def fake_organize_folder(path):
        return {"doc": 1}

    # Ensure ``src.ui.fancy_ui`` is absent
    sys.modules.pop("src.ui.fancy_ui", None)

    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))

    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"
    runpy.run_path(str(script_path), run_name="__main__")

    captured = capsys.readouterr()
    assert str({"doc": 1}) in captured.out

def test_default_ui_on_missing_module(monkeypatch, capsys):
    fake_home = Path("/no/ui/home")
    expected_downloads = fake_home / "Downloads"

    def fake_organize_folder(path):
        return {"doc": 1}

    # Ensure ``src.ui.fancy_ui`` is absent
    sys.modules.pop("src.ui.fancy_ui", None)

    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))

    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"
    runpy.run_path(str(script_path), run_name="__main__")

    captured = capsys.readouterr()
    assert str({"doc": 1}) in captured.out

def test_ui_module_overrides_default_ui(monkeypatch, capsys):
    fake_home = Path("/override/ui/home")
    expected_downloads = fake_home / "Downloads"

    def fake_organize_folder(path):
        return {"doc": 1}

    def fake_display_results(result):
        print("Overridden UI:", result)

    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))
    monkeypatch.setitem(sys.modules, "src.ui.fancy_ui", types.SimpleNamespace(display_results=fake_display_results))

    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"
    runpy.run_path(str(script_path), run_name="__main__")

    captured = capsys.readouterr()
    assert "Overridden UI: {'doc': 1}" in captured.out

def test_invalid_ui_module_does_not_crash_script(monkeypatch, capsys):
    fake_home = Path("/invalid/ui/home")
    expected_downloads = fake_home / "Downloads"

    def fake_organize_folder(path):
        return {"doc": 1}

    # Ensure ``src.ui.fancy_ui`` is invalid
    sys.modules["src.ui.fancy_ui"] = types.SimpleNamespace()

    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.setitem(sys.modules, "src.organizer", types.SimpleNamespace(organize_folder=fake_organize_folder))

    script_path = Path(__file__).resolve().parents[2] / "scripts" / "folder-organizer" / "main.py"
    runpy.run_path(str(script_path), run_name="__main__")

    captured = capsys.readouterr()
    assert str({"doc": 1}) in captured.out
```