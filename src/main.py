import os
import shutil

from copystatic import copy_files_recursive
from generate_page import generate_pages_recursive

DIR_CONTENT = "./content"
DIR_PUBLIC = "./public"
DIR_STATIC = "./static"
TEMPLATE_PATH = "template.html"


def main() -> None:
    print("Deleting public directory...")
    if os.path.exists(DIR_PUBLIC):
        shutil.rmtree(DIR_PUBLIC)

    print("Copying static files to public directory...")
    copy_files_recursive(DIR_STATIC, DIR_PUBLIC)

    print("Generating pages recursively...")
    generate_pages_recursive(DIR_CONTENT, TEMPLATE_PATH, DIR_PUBLIC)


if __name__ == "__main__":
    main()
