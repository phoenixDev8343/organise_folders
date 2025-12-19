# Contributing to `real-world-python-utilities`

Thank you for considering contributing to this repository! 🙏
This repo is a collection of **practical Python tools**. Contributions can include new utilities, improvements to existing tools, bug fixes, or documentation updates.

Please follow these guidelines to keep the project **organized, readable, and professional**.

---

## 1️⃣ Adding a New Tool

All tools live under the `scripts/` directory.
To add your tool:

1. Create a new folder under `scripts/`:

```
scripts/your_tool_name/
```

2. Inside the folder, include at minimum:

```
main.py        # entry point for your tool
README.md      # usage instructions and description
src/           # optional: modular code for your tool
json/          # optional: configuration files
```

3. Ensure your tool follows **modular design**:

   * Separate core logic (`src/`) from CLI/UI (`main.py`).
   * Optional: use `json/` for configuration instead of hardcoding values.
4. Document your tool clearly in `README.md` with:

   * Purpose / description
   * Installation instructions (dependencies)
   * Usage examples
   * Optional: configuration instructions

---

## 2️⃣ Code Style

We follow **PEP8** and Python best practices.

* **Type hints** are recommended.
* Meaningful variable/function/class names.
* Modular, readable code.
* Avoid unnecessary external dependencies; standard library preferred.

Example:

```python
from pathlib import Path

def move_file(file_path: Path, target_folder: Path) -> str:
    """Move a file to the target folder and return the folder name."""
    ...
```

---

## 3️⃣ Branching & Pull Requests

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/my-new-tool
```

3. Make your changes on that branch.
4. Run any tests or verify your tool works correctly.
5. Commit changes with a clear, concise message:

**Commit message format:**

```
feat: add <tool_name>
fix: correct <issue>
docs: update README for <tool_name>
```

6. Push your branch and open a Pull Request.

> PR description should include:
>
> * What the tool/change does
> * Usage instructions if applicable
> * Any new dependencies

---

## 4️⃣ Issues

* Bug reports, feature requests, or questions should be opened as GitHub Issues.
* Provide as much detail as possible (error messages, OS, Python version).

---

## 5️⃣ Tips for Contributors

* Test your tool independently before PR.
* Keep each PR **focused** on a single feature or fix.
* Respect existing structure (`scripts/`, `src/`, `json/`) to maintain consistency.
* Include examples in README where possible — this helps future users immediately understand your tool.

---

**Thank you for helping make `real-world-python-utilities` a useful and organized collection of Python tools!** 🚀

---

_Last updated: Oct 2025_