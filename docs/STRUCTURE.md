# Project Structure – Real World Python Utilities

## 🌳 Directory Tree (Visual Overview)

```
real-world-python-utilities/
│
├── scripts/                       # All independent Python tools
│   ├── folder-organizer/           # Folder Organizer tool
│   │   ├── main.py                 # Entry point
│   │   ├── README.md               # Tool-specific usage instructions
│   │   ├── requirements.txt        # Dependencies for this tool
│   │   ├── docs/                   # Tool-specific documentation
│   │   │   └── STRUCTURE.md
│   │   └── src/                    # Core Python modules
│   │       ├── mover.py
│   │       ├── organizer.py
│   │       ├── __init__.py
│   │       ├── json/               # Configuration files
│   │       │   └── config.json
│   │       └── ui/                 # UI modules for terminal output
│   │           ├── fancy_ui.py
│   │           └── __init__.py
│   ├── todo-cli/                    # Todo CLI tool (structure similar to folder-organizer)
│   └── ...                          # Future tools
│
├── docs/                            # Repo-wide documentation
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   ├── OVERVIEW.md
│   ├── PLAN.md
│   └── STRUCTURE.md                 # (this file)
│
├── README.md                        # Repo introduction & quick start
├── requirements.txt                 # Dependencies for all tools (if any)
└── LICENSE                          # MIT License
```

---

## 📋 Detailed Structure Table

This section provides a complete breakdown of the repository’s layout, what each folder and file does, how tools are organized, and where to find key documentation.

### 📂 Root Directory

| File/Folder          | Description                                                             |
| -------------------- | ----------------------------------------------------------------------- |
| `.gitignore`         | Specifies files and folders to be ignored by Git.                       |
| `README.md`          | Introduction, quick start instructions, and repo philosophy.            |
| `LICENSE`            | MIT License for the repository.                                         |
| `docs/`              | Documentation folder; contains repo-wide docs (`STRUCTURE.md`, etc.).   |
| `scripts/`           | Contains all independent Python utilities/projects.                     |

---

### 📂 scripts Directory

| Folder/File                                   | Description                                                     |
| --------------------------------------------- | --------------------------------------------------------------- |
| `scripts/folder-organizer/`                   | Folder Organizer tool                                           |
| `scripts/folder-organizer/main.py`            | Entry point for running the tool                                |
| `scripts/folder-organizer/README.md`          | Tool-specific instructions, usage examples, configuration notes |
| `scripts/folder-organizer/requirements.txt`   | Dependencies specific to this tool (e.g.,`rich`)                |
| `scripts/folder-organizer/docs/`              | Optional tool-specific documentation (e.g.,`STRUCTURE.md`)      |
| `scripts/folder-organizer/src/`               | Core Python modules for the tool                                |
| `scripts/folder-organizer/src/mover.py`       | Handles moving files to designated folders                      |
| `scripts/folder-organizer/src/organizer.py`   | Main logic to categorize and organize files                     |
| `scripts/folder-organizer/src/ui/`            | Modules for terminal UI and output (using `rich`)               |
| `scripts/folder-organizer/src/json/`          | Configuration files (e.g., categories for organizing files)     |
| `scripts/todo-cli/`                           | Todo CLI tool (structure similar to folder-organizer)           |

---

### 📂 docs Directory

| File                | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| `CHANGELOG.md`      | History of changes, releases, and new features                |
| `CONTRIBUTING.md`   | Guidelines for contributing, code style, and adding new tools |
| `OVERVIEW.md`       | High-level overview of the repo and included tools            |
| `PLAN.md`           | Roadmap for future utilities and planned features             |
| `STRUCTURE.md`      | Explains the repo’s file/folder structure (this file)         |

---

### 📂 scripts/folder-organizer/src Directory

| File/Folder      | Responsibility                                                                    |
| ---------------- | --------------------------------------------------------------------------------- |
| `mover.py`       | Handles moving files to their respective categorized folders.                     |
| `organizer.py`   | Contains the main logic for analyzing folders, detecting file types, and sorting. |
| `json/`          | Contains configuration files such as `config.json`.                               |
| `ui/`            | Contains modules for the user interface and display (using `rich`).               |

---

### 📂 scripts/folder-organizer/src/json Directory

| File            | Responsibility                                                          |
| --------------- | ----------------------------------------------------------------------- |
| `config.json`   | Stores categories, extensions, and user settings for file organization. |

---

### 📂 scripts/folder-organizer/src/ui Directory

| File            | Responsibility                                                       |
| --------------- | -------------------------------------------------------------------- |
| `fancy_ui.py`   | Provides user-friendly interface for displaying results and prompts. |

---

### 📝 Notes

* The repository follows **modular design**, keeping the organizing logic separate from the UI and configuration.
* The **UI folder** is isolated to maintain clean separation between interface and core logic.
* Each tool has its **own folder** inside `scripts/`, making it easy to add new utilities without breaking existing ones.
* Adding new categories, UI components, or organizing rules should follow the existing structure to ensure maintainability.

---

_Last updated: Oct 2025_