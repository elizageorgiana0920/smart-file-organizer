from pathlib import Path
import shutil
import logging

FILE_CATEGORIES = {
    "Documents": {".pdf", ".docx", ".doc", ".txt"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv"},
    "Audio": {".mp3", ".wav", ".flac"},
    "Archives": {".zip", ".rar", ".7z"},
    "Data": {".csv", ".json", ".xlsx"},
    "Code": {".py", ".cpp", ".h", ".js", ".html", ".css"},
}

logger = logging.getLogger(__name__)

def categorize_file(file_path: Path) -> str:
#returneaza categoria bazat pe tipul extensiei
    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_destination(destination: Path) -> Path:
    #genereaza un nume de fisier unic pentru a preveni suprascrierea
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        new_path = destination.with_name(new_name)

        if not new_path.exists():
            return new_path

        counter += 1


def organize_files(
    source_folder: Path,
    dry_run: bool = False
) -> dict:
    #organizeaza fisierele dupa extensie fara a le suprascrie
    if not source_folder.is_dir():
        raise NotADirectoryError(
            f"Invalid source folder: {source_folder}"
        )

    results = {
        "moved": 0,
        "skipped": 0,
        "previewed": 0,
    }

    for file_path in source_folder.iterdir():

        if not file_path.is_file():
            continue

        category = categorize_file(file_path)
        destination_folder = source_folder / category
        destination = destination_folder / file_path.name

        # Resolve filename conflicts
        destination = get_unique_destination(destination)

        if dry_run:
            logger.info(
                "[DRY RUN] %s -> %s",
                file_path.name,
                destination
            )
            results["previewed"] += 1
            continue

        destination_folder.mkdir(exist_ok=True)

        shutil.move(str(file_path), str(destination))

        results["moved"] += 1
        logger.info(
            "[MOVED] %s -> %s",
            file_path.name,
            destination
        )

    return results
