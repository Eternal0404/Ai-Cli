"""
High-level text/PDF summarization utilities.
"""

from typing import Literal

from .utils import load_text_from_path, summarize_text

SummaryLength = Literal["short", "medium", "long"]

SUMMARY_SENTENCE_MAP = {
    "short": 3,
    "medium": 7,
    "long": 12,
}


def summarize_file(path: str, length: SummaryLength = "medium") -> str:
    """
    Summarize a .txt or .pdf file.

    :param path: Path to the input file.
    :param length: One of "short", "medium", or "long".
    :return: Summary text.
    """
    if length not in SUMMARY_SENTENCE_MAP:
        raise ValueError(f"Unsupported summary length: {length}")

    text = load_text_from_path(path)
    max_sentences = SUMMARY_SENTENCE_MAP[length]
    return summarize_text(text, max_sentences=max_sentences)
