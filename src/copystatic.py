"""Static asset copying utilities."""

import os
import shutil


def copy_files_recursive(source_dir_path: str, dest_dir_path: str) -> None:
    """Recursively copy all files and directories from source to destination.

    Parameters
    ----------
    source_dir_path : str
        Path to the source directory containing assets to copy.
    dest_dir_path : str
        Path to the destination directory where assets will be written.
    """
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for item in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, item)
        dest_path = os.path.join(dest_dir_path, item)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)
