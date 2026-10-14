import argparse
import logging

from pathlib import Path
from organizer import organize_files

def main():
    parser = argparse.ArgumentParser(
        description="Organize files automatically by extension."
    )

    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Folder containing files to organize."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files."
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                "organizer.log",
                encoding="utf-8"
            )
        ]
    )

    try:
        results = organize_files(
            args.source,
            dry_run=args.dry_run
        )

    except (OSError, ValueError) as error:
        logging.error("Organization failed: %s", error)
        return 1

    print("\nOrganization completed!")
    print(f"Files moved: {results['moved']}")
    print(f"Files skipped: {results['skipped']}")
    print(f"Files previewed: {results['previewed']}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
