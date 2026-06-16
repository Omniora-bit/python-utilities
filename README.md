# 🐍 Python Utilities — Free Scripts Collection

A collection of useful, ready-to-run Python scripts for everyday file and folder tasks.

**Perfect for:** developers, sysadmins, freelancers, and anyone who works with files.

## 📜 Scripts

| Script | What it does |
|--------|-------------|
| `file_organizer.py` | Organize files by extension into subfolders (Images, Documents, Code...) |
| `batch_rename.py` | Rename multiple files at once using regex patterns |
| `duplicate_finder.py` | Find and optionally delete duplicate files by SHA256 hash |
| `folder_cleaner.py` | Remove empty folders and temp files (Thumbs.db, .log, .tmp...) |
| `image_resizer.py` | Batch resize images to max width/height (needs Pillow) |
| `csv_to_json.py` | Convert CSV files to JSON — handles headers automatically |
| `backup_script.py` | Backup folders with timestamp, optional ZIP compression |

## 🚀 Quick Start

```bash
# Organize a messy folder
python file_organizer.py ~/Downloads

# Find duplicates (safe preview)
python duplicate_finder.py ~/Documents

# Clean temp files
python folder_cleaner.py ~/Desktop

# Batch rename: replace spaces with underscores
python batch_rename.py "\s" "_" ~/Files
```

Each script has `--help` for full options:
```bash
python file_organizer.py --help
```

## 🛠 Requirements

- **Python 3.6+**
- **Pillow** only for `image_resizer.py`: `pip install Pillow`
- All others use only standard library — zero dependencies

## 📦 Want More?

This collection is a taste of my work. If you need **production-ready automation tools**, **custom scripts**, or **full project scaffolding**, check out my premium resources:

👉 **[Python Automation Scripts](https://omniora.gumroad.com/l/python-automation-scripts)** — 20+ production-ready Python scripts for file management, automation, and system tasks

👉 **[Freelance Dev Prompts](https://omniora.gumroad.com/l/freelance-dev-prompts)** — 50 battle-tested ChatGPT prompts for debugging, refactoring, testing, and more

---

*Created by [Omniora-Bit](https://github.com/Omniora-bit) — free scripts with ❤️*

## 📄 License

MIT — use freely, modify, share.
