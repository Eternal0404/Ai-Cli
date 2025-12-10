"""
Smart bulk file renamer with a simple logic fallback.
"""

import os
import re
from typing import List, Tuple


def _advanced_clean_base(base: str) -> str:
    """
    'AI-like' heuristic cleaner for a filename base (without extension).
    Attempts to make filenames human readable by:
      - Removing noise tokens (copy, final, v2, etc.).
      - Normalizing whitespace and punctuation.
    """
    # Replace common separators with spaces
    s = base.replace("_", " ").replace("-", " ").replace(".", " ")

    # Remove common noisy tokens
    s = re.sub(
        r"\b(copy|final|draft|edited|new|v\d+|version\d+|copy\s*\(\d+\))\b",
        "",
        s,
        flags=re.IGNORECASE,
    )

    # Remove parentheses/brackets content like (1), [final]
    s = re.sub(r"[\(\[\{].*?[\)\]\}]", "", s)

    # Normalize whitespace
    s = re.sub(r"\s+", " ", s).strip()

    # Lowercase and remove most punctuation
    s = s.lower()
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", "-", s)

    return s.strip("-")


def _simple_fallback_clean_base(base: str) -> str:
    """
    Simple, robust fallback that just slugifies the base name.
    """
    s = base.strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9\-\.]+", "", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-") or "file"


def build_new_filename(old_name: str) -> str:
    """
    Build a clean new filename from an existing filename.
    If 'advanced' logic fails or produces an empty name, use the simple fallback.
    """
    base, ext = os.path.splitext(old_name)
    cleaned = ""

    try:
        cleaned = _advanced_clean_base(base)
    except Exception:
        # If anything goes wrong, fall back to simple logic
        cleaned = ""

    if not cleaned:
        cleaned = _simple_fallback_clean_base(base)

    return f"{cleaned}{ext.lower()}"


def smart_bulk_rename(directory: str) -> List[Tuple[str, str]]:
    """
    Rename all files in a directory using smart cleaning rules.

    :param directory: Directory containing files to rename.
    :return: List of (old_path, new_path) pairs for renamed files.
    """
    abs_dir = os.path.abspath(directory)
    if not os.path.isdir(abs_dir):
        raise ValueError(f"Not a directory: {directory}")

    changes: List[Tuple[str, str]] = []

    for entry in os.listdir(abs_dir):
        old_path = os.path.join(abs_dir, entry)
        if not os.path.isfile(old_path):
            continue

        new_name = build_new_filename(entry)
        if new_name == entry:
            continue

        new_path = os.path.join(abs_dir, new_name)

        # Avoid collisions by appending a counter if necessary
        if os.path.exists(new_path):
            base, ext = os.path.splitext(new_name)
            counter = 1
            while True:
                candidate = os.path.join(abs_dir, f"{base}-{counter}{ext}")
                if not os.path.exists(candidate):
                    new_path = candidate
                    break
                counter += 1

        os.rename(old_path, new_path)
        changes.append((old_path, new_path))

    return changes
