# 🗂️ Folder Organizer: Smart File Sorting Script

**Folder Organizer** is a Python utility that automatically sorts your files into categorized folders based on their extensions. Using a simple JSON configuration, it moves files from a target directory (like Downloads) into dedicated folders such as Documents, Music, Pictures, Programs, and more. With a clean terminal UI powered by **Rich**, you get a clear, colorful summary of what was moved.

---

## 📑 Table of Contents

* [🗂️ Folder Organizer: Smart File Sorting Script](#-folder-organizer-smart-file-sorting-script-️)

  * [📑 Table of Contents](#-table-of-contents)
  * [🎥 Demo Video](#-demo-video)
  * [💡 Purpose &amp; Learning Goals](#-purpose--learning-goals)
  * [✨ Key Features](#-key-features)
  * [🚀 Installation](#-installation)
  * [🎮 Usage Guide](#-usage-guide)
  * [📁 Project Structure](#-project-structure)
  * [🛠️ Technologies](#-technologies)
  * [🤝🏽 Contribution](#-contribution)
  * [📃 License](#-license)
  * [🙌🏽 Acknowledgments](#-acknowledgments)

---

## 💡 Purpose & Learning Goals

This project was developed to:

* **Practice Modular Python Design:** Separates concerns into `organizer`, `mover`, and `ui` modules for maintainability.
* **Leverage JSON Configuration:** Dynamically categorize files without changing the code.
* **Use Rich for CLI UI:** Display results in colored panels for clear, user-friendly terminal output.
* **File System Automation:** Learn practical Python for real-world file organization tasks.

---

## ✨ Key Features

### File Sorting

* **Extension-Based Sorting:** Files are automatically moved into folders based on `.json` categories.
* **Default ‘Other’ Folder:** Files without a matching category are moved to an **Other** folder.
* **Customizable Categories:** Easily add, remove, or change file categories by editing `config.json`.

### Terminal UI

* **Rich Panels:** Clear, color-coded panels display each folder and the files moved.
* **Summary Information:** Shows number of files moved per folder.

### Safety & Reliability

* **Non-Destructive:** Only moves files, does not overwrite existing files.
* **Hidden Files Skipped:** Files starting with `.` are ignored to prevent accidental moves.
* **Folder Creation:** Automatically creates folders if they don’t exist.

---

## 🚀 Installation

Make sure Python 3.x is installed. Then install the required library:

```bash
# Clone the repository
git clone https://github.com/Sherouz/folder-organizer.git
```

```bash
cd folder-organizer
```

```bash
# Install required library
pip install rich
```

---

## 🎮 Usage Guide

1. **Set Up Categories:** Edit `json/config.json` to define which file types go into which folders. Example:

```json
{
    "name": "Documents",
    "extensions": [".pdf", ".docx", ".txt", ".xlsx"]
}
```

2. **Run the Organizer:**

```bash
python main.py
```

3. **Check Results:** Files in your Downloads folder will be moved into categorized folders. The terminal will display a colorful summary like this:

```
Documents (5 files):
 - report.docx
 - notes.txt
 - data.xlsx
```

---

## 📁 Project Structure

| File/Module                    | Responsibility & Design Pattern                                    |
| :----------------------------- | :----------------------------------------------------------------- |
| **`main.py`**          | Entry point. Runs the organizer and displays results.              |
| **`src/organizer.py`** | Main logic for iterating over files and assigning them to folders. |
| **`src/mover.py`**     | Moves individual files to folders; handles folder creation.        |
| **`src/ui/ui.py`**     | Rich-based CLI display of moved files in panels.                   |
| **`json/config.json`** | Defines file categories and associated extensions.                 |

---

## 🛠️ Technologies

* **Python 3.x**
* **Rich:** For terminal UI panels and colorful output.
* **Pathlib & Shutil:** Python standard libraries for file system management.

---

## 🤝🏽 Contribution

Contributions are welcome! Some ways to contribute:

1. Fork the project: `git clone <repo>`
2. Create a branch: `git checkout -b feature/new-category`
3. Make your changes (add categories, improve UI, add logging).
4. Commit: `git commit -m "feat: add new category"`
5. Push branch and open a Pull Request.

---

## 📃 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🙌🏽 Acknowledgments

* **Rich Library:** For beautiful terminal panels and UI.
* **Python Community:** Inspiration and guidance for file automation scripts.
* **Open Source Repos:** Examples and ideas from other Python CLI projects.

---

*Last updated: Oct 09, 2025*
