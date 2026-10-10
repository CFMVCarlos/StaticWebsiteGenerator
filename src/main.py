"""Command-line entry point for building the static website."""

import json
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
    try:
        basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

        print(f"Building site with basepath: '{basepath}'...")

        print("Deleting docs directory...")
        if os.path.exists(DIR_DOCS):
            shutil.rmtree(DIR_DOCS)

        print("Copying static files to docs directory...")
        copy_files_recursive(DIR_STATIC, DIR_DOCS)

        print("Generating pages recursively...")
        generate_pages_recursive(DIR_CONTENT, TEMPLATE_PATH, DIR_DOCS, basepath)

        print("Site generation complete!")

    except Exception as e:  # noqa: BLE001
        error_response = {
            "status": "error",
            "message": str(e),
            "code": 500,
            "type": type(e).__name__,
        }
        print(json.dumps(error_response, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
