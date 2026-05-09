"""
File Organizer — automatically sorts files in a directory
by type into categorized subfolders.
Usage: python file_organizer.py [--dir /path/to/folder] [--dry-run]
"""

import os
import shutil
import argparse
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

FILE_CATEGORIES = {
    "Images":      [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos":      [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"],
    "Audio":       [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Documents":   [".pdf", ".doc", ".docx", ".txt", ".odt", ".md"],
    "Spreadsheets":[".xls", ".xlsx", ".csv", ".ods"],
    "Presentations":[".ppt", ".pptx", ".key"],
    "Archives":    [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Code":        [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp"],
    "Executables": [".exe", ".dmg", ".pkg", ".sh", ".bat"],
}

def get_category(suffix: str) -> str:
    suffix = suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Misc"

def resolve_conflict(dest: Path) -> Path:
    """Append a timestamp suffix if a file already exists at dest."""
    if not dest.exists():
        return dest
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return dest.with_stem(f"{dest.stem}_{ts}")

def organize(directory: str, dry_run: bool = False) -> dict:
    base = Path(directory).resolve()
    if not base.is_dir():
        raise NotADirectoryError(f"Not a directory: {base}")

    stats = {"moved": 0, "skipped": 0, "errors": 0}

    for item in list(base.iterdir()):
        if item.is_dir() or item.name.startswith("."):
            stats["skipped"] += 1
            continue

        category = get_category(item.suffix)
        target_dir = base / category

        if not dry_run:
            target_dir.mkdir(exist_ok=True)

        dest = resolve_conflict(target_dir / item.name)
        log.info(f"[{'DRY RUN' if dry_run else 'MOVE'}] {item.name} → {category}/")
