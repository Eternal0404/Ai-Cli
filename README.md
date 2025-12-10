# ai-cli-tools

AI-powered CLI toolkit for summarizing text/PDFs, generating MCQs, converting PNG→WEBP, smart bulk renaming, and YouTube transcript summaries — fast, lightweight, and terminal-first.

## Overview

`ai-cli-tools` is a lightweight, terminal-first toolkit that brings common AI-style utilities into a single command-line interface.  
It focuses on local processing using open-source Python libraries, with simple, robust logic so it works reliably across environments.

### What it does

- **Summarize** `.txt` or `.pdf` documents into short, medium, or long summaries.
- **Generate MCQ quizzes** (5/10/20 questions) from documents, including correct answers.
- **Convert PNG → WEBP** for a single file or a whole folder.
- **Smart bulk rename** messy filenames into readable, consistent names, with a simple fallback.
- **Summarize YouTube transcripts** directly from a YouTube URL.

## Features

- Single entrypoint: `ai-cli` with subcommands.
- No proprietary APIs; uses open-source Python packages only.
- Works with plain text, PDFs, and YouTube transcripts.
- Simple frequency-based summarization (no heavyweight models required).
- Quiz generation with multiple-choice options and answer keys.
- Safe, non-destructive file renaming with collision handling.
- Cross-platform (tested on modern Python 3).

## Requirements

- Python **3.9+**
- System build tools capable of installing Python wheels (for `pypdf`, `Pillow`).
- Internet access is required for YouTube transcript fetching.

Python dependencies (also listed in `requirements.txt`):

- `pypdf`
- `Pillow`
- `youtube-transcript-api`
- `pytest` (for running tests)

Install them with:

```bash
pip install -r requirements.txt
```

## Installation

From the project root (`ai-cli-tools/`):

```bash
pip install .
```

This will install the `ai-cli` command globally in your current Python environment.

To verify the installation:

```bash
ai-cli --help
```

You should see the list of available subcommands.

## Usage

All commands follow this pattern:

```bash
ai-cli <subcommand> [options]
```

### 1. Summarizer

Summarize a text or PDF document.

**Basic usage:**

```bash
ai-cli summarize file.txt
```

**PDF with long summary:**

```bash
ai-cli summarize notes.pdf --long
```

**Available length flags:**

- `--short`
- `--medium` (default)
- `--long`

### 2. MCQ Quiz Generator

Generate multiple-choice questions from a document.

**Generate a 5-question quiz (default):**

```bash
ai-cli quiz article.pdf
```

**Generate a 10-question quiz:**

```bash
ai-cli quiz file.pdf --count 10
```

**Generate a 20-question quiz:**

```bash
ai-cli quiz notes.txt --count 20
```

Each question is printed with options `A`, `B`, `C`, `D` (or more if needed), and the correct answer is shown per question.

### 3. PNG → WEBP Converter

Convert PNG files into WEBP format.

**Convert a single PNG:**

```bash
ai-cli convert image.png
```

**Convert all PNGs in a folder to WEBP:**

```bash
ai-cli convert ./images --to webp
```

Notes:

- Only PNG → WEBP is supported currently.
- Converted files are written alongside the originals, with `.webp` extensions.

### 4. Smart Bulk Renamer

Clean up messy filenames in a directory.

```bash
ai-cli rename ./downloads
```

Behavior:

- Operates on regular files in the specified directory.
- Uses heuristic rules to:
  - Remove noise like `copy`, `final`, `v2`.
  - Normalize case and separators.
  - Produce lowercase, hyphenated, readable names.
- If the "smarter" logic fails for any reason, a simpler fallback slugification is used.
- If renaming would collide with an existing file, a numeric suffix is appended (e.g., `file-1.ext`).

### 5. YouTube Transcript Summarizer

Fetch and summarize a YouTube transcript.

**Medium-length summary (default):**

```bash
ai-cli yt https://youtu.be/xxxx
```

**Short summary:**

```bash
ai-cli yt https://www.youtube.com/watch?v=VIDEO_ID --short
```

**Long summary:**

```bash
ai-cli yt https://youtu.be/VIDEO_ID --long
```

Notes:

- Requires that the video has an available transcript (captions).
- Currently targets English transcripts (`en`).

## Development

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/ai-cli-tools.git
cd ai-cli-tools
pip install -r requirements.txt
pip install .
```

Run tests:

```bash
pytest
```

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`.
3. Make your changes, including tests where appropriate.
4. Run `pytest` and ensure all tests pass.
5. Submit a pull request with a clear description of your changes.

Please keep the code:

- Modular
- Well-documented
- Focused on open-source dependencies

## Future Roadmap

Planned improvements:

- Additional output formats (e.g., JSON export for quizzes).
- Configurable summary length by word/character count.
- Recursive renaming with dry-run mode and preview.
- Support for more file types (Markdown, HTML) in the summarizer.
- Optional integration with local ML models for more advanced summarization and question generation.
- Enhanced error reporting and logging flags in the CLI.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
