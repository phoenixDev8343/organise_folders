# 🏗️ Project Structure: Folder Organizer

This document explains the folder and file structure of the **Folder Organizer** project. It’s designed to help you understand how the code is organized and where to find each component.

---

## 📂 Root Directory

| File/Folder          | Description                                                         |
| -------------------- | ------------------------------------------------------------------- |
| `.gitignore`       | Specifies files and folders to be ignored by Git.                   |
| `main.py`          | Entry point of the application; runs the folder organizing process. |
| `README.md`        | Project documentation and instructions.                             |
| `LICENSE`          | MIT License for the project.                                        |
| `requirements.txt` | List of Python dependencies (e.g.,`pathlib`, `shutil`).         |
| `docs/`            | Documentation folder; contains `STRUCTURE.md`.                    |
| `src/`             | Source code for the folder organizer.                               |

---

## 📂 src Directory

| File/Folder      | Responsibility                                                                    |
| ---------------- | --------------------------------------------------------------------------------- |
| `mover.py`     | Handles moving files to their respective categorized folders.                     |
| `organizer.py` | Contains the main logic for analyzing folders, detecting file types, and sorting. |
| `json/`        | Contains configuration files such as `config.json`.                             |
| `ui/`          | Contains modules for the user interface and display.                              |

---

## 📂 src/json Directory

| File            | Responsibility                                                          |
| --------------- | ----------------------------------------------------------------------- |
| `config.json` | Stores categories, extensions, and user settings for file organization. |

---

## 📂 src/ui Directory

| File            | Responsibility                                                       |
| --------------- | -------------------------------------------------------------------- |
| `fancy_ui.py` | Provides user-friendly interface for displaying results and prompts. |

---

## 📝 Notes

* The project follows **modular design**, keeping the organizing logic separate from the UI and configuration.
* The **UI folder** is isolated to maintain clean separation between interface and core logic.
* Adding new categories, UI components, or organizing rules should follow the existing structure to ensure maintainability.

---

*Last updated: Oct 09, 2025*

---
