<div align="center">

# ⚡ Static Site Generator

**A minimalist Markdown-to-HTML static site generator built from scratch in Python.**

[![Live Demo](https://img.shields.io/badge/Demo-GitHub%20Pages-brightgreen?logo=github)](https://cfmvcarlos.github.io/StaticWebsiteGenerator/)
[![Python 3.13+](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/managed%20by-uv-DE5FE9?logo=astral&logoColor=white)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![Type Checked](https://img.shields.io/badge/types-basedpyright-success?logo=python)](https://github.com/DetachHead/basedpyright)
[![Docstrings](https://img.shields.io/badge/docstrings-numpy%20style-informational)](https://numpydoc.readthedocs.io/en/latest/format.html)
[![Boot.dev](https://img.shields.io/badge/curriculum-Boot.dev-orange)](https://www.boot.dev/courses/build-static-site-generator-python)

[Live Demo](https://cfmvcarlos.github.io/StaticWebsiteGenerator/) • [Features](#-features) • [Architecture](#-architecture) • [Getting Started](#-getting-started) • [CLI Commands](#-cli-commands) • [Verification](#-code-quality--verification)

---

</div>

## 📖 Overview

**StaticSiteGenerator** is a lightweight, zero-dependency static site generator implemented from first principles in modern Python 3.13. Rather than relying on external markdown compilation libraries or heavyweight frameworks, it constructs its own Abstract Syntax Tree (AST), parses inline and block-level Markdown constructs, and generates static HTML files bound to custom page templates.

The project demonstrates tree data structures, recursive file traversal, tokenization, regular expression parsing, and automated static asset bundling.

---

## ✨ Features

- 🌲 **Custom Abstract Syntax Tree (AST):** Object-oriented node hierarchy featuring [`HTMLNode`](file:///home/cfmv/BootDev/StaticWebsiteGenerator/src/htmlnode.py#L4), [`LeafNode`](file:///home/cfmv/BootDev/StaticWebsiteGenerator/src/htmlnode.py#L77), and [`ParentNode`](file:///home/cfmv/BootDev/StaticWebsiteGenerator/src/htmlnode.py#L125) with recursive HTML compilation.
- 🔤 **Inline Markdown Parsing:** Splits and tokenizes inline formatting including **bold** (`**`), *italic* (`*` and `_`), `code` (` ` `), hyperlinks (`[text](url)`), and images (`![alt](url)`).
- 🧱 **Block-Level Syntax Engine:** Distinguishes and converts paragraphs, multi-level headings (`h1` through `h6`), fenced code blocks (`<pre><code>`), blockquotes (`<blockquote>`), unordered lists (`<ul>`), and sequentially ordered lists (`<ol>`).
- 📁 **Recursive Directory Crawling:** Automatically crawls nested directory hierarchies (`content/`) and replicates the exact folder structure when rendering HTML files into the target destination (`docs/` or `public/`).
- 🎨 **Static Asset Synchronization:** Rebuilds destination asset directories cleanly by recursively copying images, stylesheets, and media from `static/`.
- 🌐 **GitHub Pages Ready:** Full support for configurable root basepaths (e.g. `/StaticWebsiteGenerator/`), rewriting internal `href` and `src` attributes for subdirectory hosting.
- 🛡️ **Comprehensive Verification Bar:** Fully typed with modern Python annotations, verified against `basedpyright`, formatted and linted with `ruff`, validated for NumPy docstring compliance with `pydoclint`, and covered by 98 unit tests.

---

## 🏛️ Architecture

```
StaticWebsiteGenerator/
├── scripts/
│   ├── build.sh              # Builds site with GitHub Pages basepath (/StaticWebsiteGenerator/)
│   ├── main.sh               # Builds site locally with basepath / and starts dev server (port 8888)
│   └── test.sh               # Runs unittest discovery across all unit test suites
├── template.html             # Base HTML document template containing {{ Title }} and {{ Content }}
├── content/                  # Markdown source files
│   ├── index.md              # Homepage content
│   ├── contact/
│   │   └── index.md          # Contact page
│   └── blog/
│       ├── glorfindel/       # Blog post: Glorfindel
│       ├── majesty/          # Blog post: The Majesty of the Trees
│       └── tom/              # Blog post: Tom Bombadil
├── static/                   # Static assets (stylesheets, images)
│   ├── index.css             # Main stylesheet
│   └── images/               # Image assets (PNG)
├── docs/                     # Generated static site (served by GitHub Pages)
└── src/                      # Core generator source code
    ├── htmlnode.py           # HTMLNode, LeafNode, ParentNode AST classes
    ├── textnode.py           # TextNode and TextType enum with HTML converter
    ├── splitnode.py          # Inline markdown tokenization and delimiter splitting
    ├── splitblock.py         # Block-level classification and markdown-to-HTML AST parser
    ├── copystatic.py         # Recursive asset directory copy utilities
    ├── generate_page.py      # Template hydration and recursive page generators
    ├── main.py               # Application entrypoint and pipeline orchestrator
    ├── test_htmlnode.py      # Unit tests for AST node classes
    ├── test_textnode.py      # Unit tests for TextNode representations
    ├── test_splitnode.py     # Unit tests for inline tokenization logic
    └── test_splitblock.py    # Unit tests for block-level parsing and AST generation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or newer
- [uv](https://github.com/astral-sh/uv) (recommended) or standard `pip`

### Installation

Clone the repository and sync development dependencies:

```bash
git clone https://github.com/CFMVCarlos/StaticWebsiteGenerator.git
cd StaticWebsiteGenerator

# Install tools with uv
uv sync
```

Alternatively, using standard Python `venv`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## 💻 CLI Commands

The repository provides automated bash shell scripts for common tasks:

| Command | Action | Description |
|---|---|---|
| `./scripts/main.sh` | **Local Development** | Compiles site with basepath `"/"` to `docs/` and starts an HTTP server at `http://localhost:8888` |
| `./scripts/build.sh` | **Production Build** | Compiles site with basepath `"/StaticWebsiteGenerator/"` for GitHub Pages |
| `./scripts/test.sh` | **Run Tests** | Executes all 98 unit tests via Python's standard `unittest` framework |

You can also run the generator directly via Python:

```bash
# Build for local preview (root basepath)
uv run python3 src/main.py "/"

# Build for custom subdirectory deployment
uv run python3 src/main.py "/StaticWebsiteGenerator/"
```

---

## 🧪 Code Quality & Verification

The codebase adheres to strict linting, type-checking, and docstring guidelines:

```bash
# 1. Run unit test suite (98 tests)
./scripts/test.sh

# 2. Lint and format checks
uv run ruff check
uv run ruff format --check

# 3. NumPy docstring validation
uv run pydoclint .

# 4. Type checking
uv run ty check
uv run basedpyright
```

---

## 🌐 Live Deployment

The site is automatically deployed to GitHub Pages at:

🔗 **[https://cfmvcarlos.github.io/StaticWebsiteGenerator/](https://cfmvcarlos.github.io/StaticWebsiteGenerator/)**

---

## 📜 License & Credits

Built by [Carlos](https://github.com/CFMVCarlos) as part of the [Boot.dev](https://www.boot.dev/) curriculum on Functional Programming and Static Site Generators.

## Development

To enable automated commit message validation with gitlint:
```bash
git config core.hooksPath .githooks
```

