"""
YouTube transcript fetcher and summarizer.
"""

from typing import List, Optional
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)


def _get_transcript_entries(video_id: str, languages: list[str]) -> list[dict]:
    """Return transcript entries for a video, compatible with multiple
    versions of ``youtube-transcript-api``.

    Newer versions (>=1.x) expose an instance API with ``fetch`` returning a
    ``FetchedTranscript``. Older versions provide the class method
    ``YouTubeTranscriptApi.get_transcript`` returning a list of dicts.
    """
    # Try modern instance API first
    try:
        api = YouTubeTranscriptApi()  # type: ignore[call-arg]
    except TypeError:
        api = None

    if api is not None and hasattr(api, "fetch"):
        fetched = api.fetch(video_id, languages=tuple(languages))  # type: ignore[arg-type]
        # ``FetchedTranscript`` provides ``to_raw_data``; fall back to the
        # object itself if the interface changes again.
        if hasattr(fetched, "to_raw_data"):
            return fetched.to_raw_data()  # type: ignore[no-any-return]
        return fetched  # type: ignore[no-any-return]

    # Fallback to legacy class method API
    if hasattr(YouTubeTranscriptApi, "get_transcript"):
        return YouTubeTranscriptApi.get_transcript(video_id, languages=languages)  # type: ignore[no-any-return]

    raise RuntimeError(
        "Installed youtube-transcript-api version is not supported: "
        "no usable transcript fetch method found."
    )

from .utils import normalize_whitespace, summarize_text
from .summarizer import SUMMARY_SENTENCE_MAP


def extract_video_id(url: str) -> str:
    """
    Extract a YouTube video ID from a variety of URL formats.
    """
    parsed = urlparse(url)

    # Short links: https://youtu.be/<id>
    if "youtu.be" in parsed.netloc:
        vid = parsed.path.lstrip("/")
        if vid:
            return vid

    # Standard watch URLs: https://www.youtube.com/watch?v=<id>
    if "youtube.com" in parsed.netloc:
        query = parse_qs(parsed.query)
        if "v" in query and query["v"]:
            return query["v"][0]

        # Embedded or shorts-style: /embed/<id>, /shorts/<id>
        parts = parsed.path.strip("/").split("/")
        for marker in ("embed", "shorts"):
            if marker in parts:
                idx = parts.index(marker)
                if idx + 1 < len(parts):
                    return parts[idx + 1]

    raise ValueError(f"Could not extract a YouTube video ID from URL: {url}")


def fetch_transcript_text(video_id: str, languages: Optional[List[str]] = None) -> str:
    """Fetch transcript text for a YouTube video ID.

    This handles both legacy and modern versions of ``youtube-transcript-api``.
    """
    languages = languages or ["en"]
    try:
        transcript_entries = _get_transcript_entries(video_id, languages)
    except (TranscriptsDisabled, NoTranscriptFound) as exc:
        raise RuntimeError(f"No transcript available for video {video_id}: {exc}") from exc

    text_parts = [item.get("text", "") for item in transcript_entries]
    return normalize_whitespace(" ".join(text_parts))


def summarize_youtube_url(url: str, length: str = "medium") -> str:
    """
    Fetch a YouTube transcript and summarize it.
    """
    if length not in SUMMARY_SENTENCE_MAP:
        raise ValueError(f"Unsupported summary length: {length}")

    video_id = extract_video_id(url)
    transcript = fetch_transcript_text(video_id)
    max_sentences = SUMMARY_SENTENCE_MAP[length]
    return summarize_text(transcript, max_sentences=max_sentences)
