from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).parent
readme_path = here / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""


setup(
    name="ai-cli-tools",
    version="0.1.0",
    description=(
        "AI-powered CLI toolkit for summarizing text/PDFs, generating MCQs, converting PNG→WEBP, "
        "smart bulk renaming, and YouTube transcript summaries — fast, lightweight, and terminal-first."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/yourusername/ai-cli-tools",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.9",
    install_requires=[
        "pypdf>=4.0.0",
        "Pillow>=10.0.0",
        "youtube-transcript-api>=0.6.2",
    ],
    entry_points={
        "console_scripts": [
            "ai-cli=ai_cli.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Text Processing :: General",
    ],
    include_package_data=True,
    zip_safe=False,
)
