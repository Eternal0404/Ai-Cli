import os
import re
from typing import Dict, List

from pypdf import PdfReader

# A minimal English stopword list for basic NLP-style processing.
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "he",
    "her",
    "his",
    "i",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "there",
    "they",
    "this",
    "to",
    "was",
    "were",
    "will",
    "with",
    "you",
    "your",
}


def read_text_file(path: str) -> str:
    """
    Read a UTF-8 (or similar) text file and return its contents as a string.
    Falls back to latin-1 if UTF-8 decoding fails.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    for encoding in ("utf-8", "latin-1"):
        try:
            with open(path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue

    # Last resort: ignore errors
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def read_pdf_file(path: str) -> str:
    """
    Extract text from a PDF file using pypdf.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    reader = PdfReader(path)
    texts: List[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        texts.append(page_text)
    return "\n".join(texts)


def load_text_from_path(path: str) -> str:
    """
    Load text content from a supported file type (.txt, .pdf).
    """
    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext == ".txt":
        return read_text_file(path)
    if ext == ".pdf":
        return read_pdf_file(path)

    raise ValueError(f"Unsupported file type: {ext}. Expected .txt or .pdf.")


def normalize_whitespace(text: str) -> str:
    """
    Collapse consecutive whitespace into single spaces and trim.
    """
    return re.sub(r"\s+", " ", text or "").strip()


def split_sentences(text: str) -> List[str]:
    """
    Naive sentence splitter based on punctuation.
    """
    text = normalize_whitespace(text)
    if not text:
        return []
    # Split on punctuation followed by whitespace
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def _build_word_frequencies(sentences: List[str]) -> Dict[str, int]:
    """
    Build a simple word frequency dictionary for non-stopwords.
    """
    freqs: Dict[str, int] = {}
    for sentence in sentences:
        for token in re.findall(r"\w+", sentence.lower()):
            if token in STOPWORDS or len(token) <= 2:
                continue
            freqs[token] = freqs.get(token, 0) + 1
    return freqs


def summarize_text(text: str, max_sentences: int = 5) -> str:
    """
    Frequency-based extractive summarizer.
    Chooses the top-N scored sentences and preserves original order.
    """
    text = normalize_whitespace(text)
    sentences = split_sentences(text)
    if not sentences:
        return ""

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    freqs = _build_word_frequencies(sentences)
    if not freqs:
        # Fallback: just take the first N sentences
        return " ".join(sentences[:max_sentences])

    scored_sentences = []
    for idx, sentence in enumerate(sentences):
        tokens = re.findall(r"\w+", sentence.lower())
        score = sum(freqs.get(tok, 0) for tok in tokens)
        scored_sentences.append((score, idx, sentence))

    # Pick top sentences by score
    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    top = sorted(scored_sentences[:max_sentences], key=lambda x: x[1])

    return " ".join(sentence for _, _, sentence in top)
