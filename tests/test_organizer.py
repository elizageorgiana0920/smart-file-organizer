from pathlib import Path
import pytest
from organizer import (
    categorize_file,
    get_unique_destination,
    organize_files,
)

# 1. Test file categorization
@pytest.mark.parametrize(
    "filename, expected",
    [
        ("CV.pdf", "Documents"),
        ("photo.JPG", "Images"),
        ("video.mp4", "Videos"),
        ("music.mp3", "Audio"),
        ("archive.zip", "Archives"),
        ("data.csv", "Data"),
        ("script.py", "Code"),
        ("unknown.xyz", "Others"),
    ],
)

def test_categorize_file(filename, expected):
    assert categorize_file(Path(filename)) == expected

# 2. Test unique filename generation
def test_unique_destination(tmp_path):
    existing = tmp_path / "CV.pdf"
    existing.write_text("Original")

    destination = get_unique_destination(existing)

    assert destination == tmp_path / "CV_1.pdf"

# 3. Test multiple filename conflicts
def test_multiple_duplicates(tmp_path):
    (tmp_path / "CV.pdf").touch()
    (tmp_path / "CV_1.pdf").touch()

    destination = get_unique_destination(
        tmp_path / "CV.pdf"
    )

    assert destination == tmp_path / "CV_2.pdf"

# 4. Test actual file organization
def test_organize_files(tmp_path):
    (tmp_path / "notes.pdf").write_text("Test document")
    (tmp_path / "photo.jpg").write_text("Test image")

    results = organize_files(tmp_path)

    assert results["moved"] == 2
    assert (tmp_path / "Documents" / "notes.pdf").exists()
    assert (tmp_path / "Images" / "photo.jpg").exists()

    assert not (tmp_path / "notes.pdf").exists()
    assert not (tmp_path / "photo.jpg").exists()

# 5. Test dry-run mode
def test_dry_run(tmp_path):
    source = tmp_path / "CV.pdf"
    source.write_text("Important document")

    results = organize_files(tmp_path, dry_run=True)

    assert results["moved"] == 0
    assert results["previewed"] == 1

    assert source.exists()
    assert not (tmp_path / "Documents").exists()


# 6. Test duplicate handling during organization
def test_duplicate_organization(tmp_path):
    documents = tmp_path / "Documents"
    documents.mkdir()

    (documents / "CV.pdf").write_text("Original")
    (tmp_path / "CV.pdf").write_text("New")

    results = organize_files(tmp_path)

    assert results["moved"] == 1

    assert (documents / "CV.pdf").read_text() == "Original"
    assert (documents / "CV_1.pdf").read_text() == "New"


# 7. Test invalid source directory
def test_invalid_directory(tmp_path):
    missing_folder = tmp_path / "missing"

    with pytest.raises(NotADirectoryError):
        organize_files(missing_folder)


# 8. Test that directories are ignored
def test_ignore_directories(tmp_path):
    (tmp_path / "SomeFolder").mkdir()

    results = organize_files(tmp_path)

    assert results["moved"] == 0
    assert (tmp_path / "SomeFolder").is_dir()


# 9. Test unknown extensions
def test_unknown_extension(tmp_path):
    (tmp_path / "mystery.abc").write_text("Unknown file")

    organize_files(tmp_path)

    assert (tmp_path / "Others" / "mystery.abc").exists()
