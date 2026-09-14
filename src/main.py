"""Command-line entry point for building the static website."""

import os
import shutil
import sys

from copystatic import copy_files_recursive
from generate_page import generate_pages_recursive

DIR_CONTENT = "./content"
DIR_DOCS = "./docs"
DIR_STATIC = "./static"
TEMPLATE_PATH = "template.html"


def main() -> None:
    """Execute site generation by copying static assets and compiling markdown."""
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print(f"Building site with basepath: '{basepath}'...")

    print("Deleting docs directory...")
    if os.path.exists(DIR_DOCS):
        shutil.rmtree(DIR_DOCS)

    print("Copying static files to docs directory...")
    copy_files_recursive(DIR_STATIC, DIR_DOCS)

    print("Generating pages recursively...")
    generate_pages_recursive(DIR_CONTENT, TEMPLATE_PATH, DIR_DOCS, basepath)


if __name__ == "__main__":
    main()
