"""
Command-line interface for ai-cli-tools.

Commands:
  ai-cli summarize <file>
  ai-cli summarize <file> --long
  ai-cli quiz <file> --count 10
  ai-cli convert <file_or_dir> --to webp
  ai-cli rename <directory>
  ai-cli yt <youtube_url> [--short|--medium|--long]
"""

import argparse
import sys
from typing import List

from .summarizer import summarize_file
from .quiz_generator import generate_mcqs_from_file, MCQ
from .converter import convert_png_to_webp
from .renamer import smart_bulk_rename
from .youtube_summary import summarize_youtube_url


def _resolve_length_from_flags(args) -> str:
    """
    Map mutually exclusive flags to one of: short, medium, long.
    """
    if getattr(args, "short", False):
        return "short"
    if getattr(args, "long", False):
        return "long"
    if getattr(args, "medium", False):
        return "medium"
    return "medium"


def _add_length_flags(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--short", action="store_true", help="Short summary.")
    group.add_argument("--medium", action="store_true", help="Medium summary (default).")
    group.add_argument("--long", action="store_true", help="Long summary.")


def handle_summarize(args: argparse.Namespace) -> int:
    length = _resolve_length_from_flags(args)
    try:
        summary = summarize_file(args.path, length=length)
    except Exception as exc:  # noqa: BLE001
        print(f"Error summarizing file: {exc}", file=sys.stderr)
        return 1

    print(summary)
    return 0


def _format_mcqs_for_cli(mcqs: List[MCQ]) -> str:
    lines: List[str] = []
    for i, mcq in enumerate(mcqs, start=1):
        lines.append(f"Q{i}. {mcq.question}")
        for idx, option in enumerate(mcq.options):
            label = chr(ord("A") + idx)
            lines.append(f"  {label}. {option}")
        correct_letter = chr(ord("A") + mcq.answer_index)
        lines.append(f"Answer: {correct_letter}")
        lines.append("")  # blank line between questions
    return "\n".join(lines).rstrip() + "\n"


def handle_quiz(args: argparse.Namespace) -> int:
    try:
        mcqs = generate_mcqs_from_file(args.path, num_questions=args.count)
    except Exception as exc:  # noqa: BLE001
        print(f"Error generating quiz: {exc}", file=sys.stderr)
        return 1

    if not mcqs:
        print("Could not generate any questions from the input (text may be too short).", file=sys.stderr)
        return 1

    print(_format_mcqs_for_cli(mcqs))
    return 0


def handle_convert(args: argparse.Namespace) -> int:
    try:
        conversions = convert_png_to_webp(args.path, to_format=args.to)
    except Exception as exc:  # noqa: BLE001
        print(f"Error converting images: {exc}", file=sys.stderr)
        return 1

    if not conversions:
        print("No PNG files were converted (nothing to do).", file=sys.stderr)
        return 1

    for src, dst in conversions:
        print(f"Converted {src} -> {dst}")
    return 0


def handle_rename(args: argparse.Namespace) -> int:
    try:
        changes = smart_bulk_rename(args.path)
    except Exception as exc:  # noqa: BLE001
        print(f"Error renaming files: {exc}", file=sys.stderr)
        return 1

    if not changes:
        print("No files were renamed (directory may be empty or already clean).")
        return 0

    for old, new in changes:
        print(f"{old} -> {new}")
    return 0


def handle_youtube(args: argparse.Namespace) -> int:
    length = _resolve_length_from_flags(args)
    try:
        summary = summarize_youtube_url(args.url, length=length)
    except Exception as exc:  # noqa: BLE001
        print(f"Error summarizing YouTube video: {exc}", file=sys.stderr)
        return 1

    print(summary)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-cli",
        description=(
            "AI-powered CLI toolkit for summarizing text/PDFs, generating MCQs, "
            "converting PNG→WEBP, smart bulk renaming, and YouTube transcript summaries "
            "— fast, lightweight, and terminal-first."
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # summarize
    summarize_parser = subparsers.add_parser("summarize", help="Summarize a text or PDF file.")
    summarize_parser.add_argument("path", help="Path to .txt or .pdf file.")
    _add_length_flags(summarize_parser)
    summarize_parser.set_defaults(func=handle_summarize)

    # quiz
    quiz_parser = subparsers.add_parser("quiz", help="Generate MCQs from a text or PDF file.")
    quiz_parser.add_argument("path", help="Path to .txt or .pdf file.")
    quiz_parser.add_argument(
        "--count",
        type=int,
        choices=[5, 10, 20],
        default=5,
        help="Number of questions to generate (5, 10, or 20).",
    )
    quiz_parser.set_defaults(func=handle_quiz)

    # convert
    convert_parser = subparsers.add_parser("convert", help="Convert PNG images to WEBP.")
    convert_parser.add_argument("path", help="Path to a .png file or a directory of .png files.")
    convert_parser.add_argument(
        "--to",
        default="webp",
        choices=["webp"],
        help="Target format (currently only 'webp' is supported).",
    )
    convert_parser.set_defaults(func=handle_convert)

    # rename
    rename_parser = subparsers.add_parser("rename", help="Smart bulk-rename files in a directory.")
    rename_parser.add_argument("path", help="Directory whose files will be renamed.")
    rename_parser.set_defaults(func=handle_rename)

    # yt
    yt_parser = subparsers.add_parser("yt", help="Summarize a YouTube video's transcript.")
    yt_parser.add_argument("url", help="YouTube video URL.")
    _add_length_flags(yt_parser)
    yt_parser.set_defaults(func=handle_youtube)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return 1
    return func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
