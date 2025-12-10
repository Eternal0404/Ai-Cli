"""
PNG → WEBP image conversion utilities.
"""

import os
from typing import List, Tuple

from PIL import Image


def _convert_single_png_to_webp(src_path: str, dst_path: str) -> None:
    """
    Convert a single PNG file to WEBP format.
    """
    os.makedirs(os.path.dirname(dst_path) or ".", exist_ok=True)
    with Image.open(src_path) as img:
        img.save(dst_path, format="WEBP")


def convert_png_to_webp(path: str, to_format: str = "webp") -> List[Tuple[str, str]]:
    """
    Convert a single PNG file or all PNGs in a directory to WEBP.

    :param path: Path to a .png file or a directory containing .png files.
    :param to_format: Currently only 'webp' is supported.
    :return: List of (source_path, destination_path) pairs for converted files.
    """
    to_format = to_format.lower()
    if to_format != "webp":
        raise ValueError("Only conversion to WEBP is supported (use --to webp).")

    abs_path = os.path.abspath(path)
    converted: List[Tuple[str, str]] = []

    if os.path.isdir(abs_path):
        for entry in os.listdir(abs_path):
            src = os.path.join(abs_path, entry)
            if not os.path.isfile(src):
                continue
            if not entry.lower().endswith(".png"):
                continue
            dst = os.path.splitext(src)[0] + ".webp"
            _convert_single_png_to_webp(src, dst)
            converted.append((src, dst))
    else:
        if not abs_path.lower().endswith(".png"):
            raise ValueError("Input must be a .png file or a directory containing .png files.")
        dst = os.path.splitext(abs_path)[0] + ".webp"
        _convert_single_png_to_webp(abs_path, dst)
        converted.append((abs_path, dst))

    return converted
