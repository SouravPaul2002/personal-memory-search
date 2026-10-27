import os
from pathlib import Path
from typing import Iterable


def norm_path(path: str) -> str:
    """Returns canonical normalized absolute path (casing and slashes normalized)."""
    return os.path.normcase(os.path.abspath(path))


def is_file_in_dir(file_path: str, dir_path: str, recursive: bool = True) -> bool:
    """
    Checks if file_path is located inside dir_path.
    If recursive is False, only immediate children of dir_path match.
    If recursive is True, any nested descendant of dir_path matches.
    """
    try:
        norm_file = norm_path(file_path)
        norm_dir = norm_path(dir_path)
        if norm_file == norm_dir:
            return False
        if not recursive:
            return os.path.dirname(norm_file) == norm_dir
        return Path(norm_file).is_relative_to(Path(norm_dir))
    except Exception:
        return False


def is_file_in_folders(file_path: str, folders: Iterable[str], recursive: bool = False) -> bool:
    """Checks if file_path is located inside any of the specified folders."""
    return any(is_file_in_dir(file_path, folder, recursive=recursive) for folder in folders)
