# **💠 Real World Python Utilities**

`real-world-python-utilities` is a collection of **small yet practical Python tools** built to automate repetitive tasks, organize files, and simplify daily workflows.
Each tool is **lightweight, modular, and easy to use**, making this repo ideal for learning, personal productivity, or inspiration for your own automation scripts.

---

## 📑 Table of Contents

* [💠 Real World Python Utilities](#-real-world-python-utilities)
  * [📑 Table of Contents](#-table-of-contents)
  * [🧠 Overview](#-overview)
  * [🗂️ Structure](#-structure)
    * [Example Project: Folder Organizer](#example-project-folder-organizer)
  * [⚙️ Quick Start / Usage](#-quick-start--usage)
    * [Clone the Repository](#clone-the-repository)
    * [Install Project Dependencies](#install-project-dependencies)
    * [Run a Project](#run-a-project)
  * [🧩 Included Tools](#-included-tools)
  * [🧰 Philosophy](#-philosophy)
  * [🛠️ Installation Notes](#-installation-notes)
  * [📚 Contribution & Adding Your Own Utilities](#-contribution--adding-your-own-utilities)
  * [🔗 Resources & References](#-resources--references)
  * [📂 Documentation](#-documentation)
  * [📃 License](#-license)
  * [🧑‍💻 Author](#-author)
  * [⚡ Tips for Users](#-tips-for-users)


---

## 🧠 Overview

This repository contains independent Python scripts designed to handle common automation needs — such as:

* File organization and sorting
* Todo/task management
* Text processing
* Small utility scripts for everyday tasks

Each tool is designed to do **one thing well**, with minimal dependencies and clear CLI usage. The focus is on **real-world utility**, readability, and maintainability.

---

## 🗂️ Structure

Each project lives in its own folder. Typical structure:

```
scripts/project_name/
│
├── main.py           # main script, entry point
├── README.md         # description & usage instructions
├── src/              # source code modules
└── json/             # optional configuration files
```

Example of included project:

```
scripts/folder_organizer/
```

> Each project may include subfolders for modular code (`src/`) and configuration (`json/`) to keep things organized.

---

## ⚙️ Quick Start / Usage

1. **Clone the repository**

```bash
git clone https://github.com/Sherouz/real-world-python-utilities.git
cd real-world-python-utilities
```

2. **Install requirements (if needed)**

Each project manages its own dependencies.  
Navigate into the project folder and install its requirements if available:

```bash
cd scripts/folder_organizer
pip install -r requirements.txt
```

> Most projects rely only on Python's **standard library**. Additional dependencies (like `rich`) are listed in `requirements.txt`.

3. **Run a project**

```bash
python scripts/folder_organizer/main.py
```

> Each project is independent, you can run any script directly. Check the README inside each project for detailed usage instructions.

---

## 🧩 Included Tools

| Tool                               | Description                                          |
| ---------------------------------- | ---------------------------------------------------- |
| **Folder Organizer**         | Automatically sorts files into folders by extension. |
| *(More utilities coming soon…)* | Stay tuned for updates and new tools!                |

---

## 🧰 Philosophy

We follow **three core principles** in this repo:

1. **Keep it simple:** Each tool should do one thing and do it well.
2. **Make it modular:** Clean separation between UI, logic, and configuration.
3. **Ensure practical usefulness:** Only real-world utility scripts are included; experiments and mini games are kept separate.

This approach keeps the code **readable, maintainable, and reusable**, whether you are a beginner learning Python or a developer looking for ready-made automation tools.

---

## 🛠️ Installation Notes

* Python 3.10+ is recommended.
* Standard library tools are used wherever possible.
* Additional dependencies are listed per project.
* Tools are **non-destructive**: files are moved, not overwritten. Hidden files are ignored unless specified.

---

## 📚 Contribution & Adding Your Own Utilities

Contributions are welcome! You can:

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-tool`
3. Add your tool inside scripts/ with a main.py and README.md
4. Make sure it follows the **modular + minimal dependency** principle
5. Open a Pull Request

> Include a brief description of your tool, its usage, and any dependencies in the README of your project.

---

## 🔗 Resources & References

* [Python Standard Library Documentation](https://docs.python.org/3/library/)
* [Rich Documentation](https://rich.readthedocs.io/en/stable/)
* Open source Python CLI projects for inspiration

---

## 📂 Documentation

The repository includes detailed documentation in the `docs/` folder. You can access each file directly:

* **[`CHANGELOG.md`](docs/CHANGELOG.md)** – Record of version updates and changes.
* **[`CONTRIBUTING.md`](docs/CONTRIBUTING.md)** – Guidelines for contributing to the repository.
* **[`OVERVIEW.md`](docs/OVERVIEW.md)** – Overview of the project’s purpose, goals, and scope.
* **[`PLAN.md`](docs/PLAN.md)** – Roadmap and planned features for the project.
* **[`STRUCTURE.md`](docs/STRUCTURE.md)** – Complete map of files and directories in the repository.

> These documents provide essential information to understand, use, and contribute to the repository effectively.

---

## 📃 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🧑‍💻 Author

Developed and maintained by **[Shahrouz](https://github.com/Sherouz)**.
Focused on building practical tools and automation scripts using **pure Python**, with emphasis on **modular design, clarity, and usability**.

---

## ⚡ Tips for Users

* Customize each tool via its `config.json` (if available) to fit your workflow.
* Explore each project folder for examples and additional functionality.
* Combine multiple tools for more complex automation workflows.

---

*Last updated: Oct 09, 2025*

```

```
