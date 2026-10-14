# Smart File Organizer

**Python | File Automation | Command-Line Interface | Logging | pytest**

A lightweight Python command-line tool that organizes files into category folders based on their extensions. It includes a safe preview mode, automatic filename conflict resolution, operation logging, and automated tests.

## Features

- **Extension-based categorization:** sorts documents, images, videos, audio, archives, data files, source code, and unknown file types.
- **Automatic organization:** moves files into category subfolders within the selected source directory.
- **Duplicate filename protection:** if the destination already contains a file with the same name, generates a suffix such as `report_1.pdf` instead of overwriting it.
- **Dry-run mode:** previews proposed moves without creating folders or moving files.
- **CLI:** accepts a source directory and an optional `--dry-run` flag.
- **Logging:** writes operations to the terminal and to `organizer.log`.
- **Automated tests:** pytest tests cover categorization, duplicates, file moves, preview mode, invalid paths, and directory skipping.

## How It Works

**Before:**

```text
sample_files/
├── report.pdf
├── birthday.jpg
├── calendar.csv
└── project.zip
```

**After:**

```text
sample_files/
├── Documents/
│   └── report.pdf
├── Images/
│   └── birthday.jpg
├── Data/
│   └── calendar.csv
└── Archives/
    └── project.zip
```

The organizer processes regular files immediately inside the chosen directory. Existing subdirectories are skipped (the tool is **not recursive**).

## Requirements

- Python 3.11+ recommended
- `pytest` for development/testing (the organizer itself uses only the Python standard library)

## Getting Started

Clone the repository and enter the project directory:

```bash
git clone https://github.com/USERNAME/smart-file-organizer.git
cd smart-file-organizer
```

Optionally create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install test dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

**Always preview first**, particularly when working with important files:

```bash
python main.py --source sample_files --dry-run
```

To perform the moves:

```bash
python main.py --source sample_files
```

To view CLI options:

```bash
python main.py --help
```

Example preview output:

```text
INFO | [DRY RUN] birthday.jpg -> sample_files/Images/birthday.jpg
INFO | [DRY RUN] calendar.csv -> sample_files/Data/calendar.csv

Organization completed!
Files moved: 0
Files skipped: 0
Files previewed: 2
```

Windows users can also pass a quoted absolute path, for example:

```powershell
python main.py --source "C:\Users\YourName\Downloads" --dry-run
```

**Warning:** Without `--dry-run`, this program actually moves files. Test on a disposable directory first; there is currently no undo feature.

## File Categories

| Destination | Extensions |
| --- | --- |
| Documents | `.pdf`, `.docx`, `.doc`, `.txt` |
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp` |
| Videos | `.mp4`, `.mov`, `.avi`, `.mkv` |
| Audio | `.mp3`, `.wav`, `.flac` |
| Archives | `.zip`, `.rar`, `.7z` |
| Data | `.csv`, `.json`, `.xlsx` |
| Code | `.py`, `.cpp`, `.h`, `.js`, `.html`, `.css` |
| Others | all other extensions |

Extension matching is case-insensitive.

## Project Structure

```text
smart-file-organizer/
├── main.py                 # argparse CLI and logging setup
├── organizer.py            # classification and file-moving logic
├── tests/
│   └── test_organizer.py   # automated pytest tests
├── requirements.txt        # development/test dependency
├── .gitignore
└── README.md
```

A local `sample_files/` directory can be created for demonstration; it does not need to be committed to Git.

## Testing

Run all tests from the project root:

```bash
python -m pytest -v
```

The suite checks file categories, name collision handling, real moves in temporary directories, dry-run behavior, invalid source paths, and skipped subdirectories. `pytest`'s `tmp_path` fixture isolates test data from personal files.

## Design Notes and Limitations

- The implementation relies on Python's `pathlib`, `shutil`, `argparse`, and `logging` modules.
- Files are classified by **extension only**, not by inspecting their actual content.
- Directory traversal is non-recursive.
- When a name already exists in the target folder, the tool appends a numeric suffix. It does **not** detect identical file contents.
- Dry-run is a preview, not a reservation system; file changes between preview and execution can alter the final destination.
- The tool does not provide undo, atomic multi-file moves, or a full recovery mechanism for partial failures.
- The existing `skipped` result counter is retained for potential future policies, but the current implementation typically renames conflicts rather than skipping them.

## Possible Improvements

- Structured per-file error handling and summary reporting.
- An optional undo manifest for completed moves.
- Hash-based duplicate content detection.
- Recursive mode and user-configurable category rules.
- CI to run pytest on every push and pull request.

## Author

**Eliza-Georgiana Boroș**  
Computer Science Student, University of Bucharest  
[GitHub](https://github.com/elizageorgiana0920)
