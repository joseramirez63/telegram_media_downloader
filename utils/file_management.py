"""Utility functions to handle downloaded files."""

import glob
import os
import pathlib
import urllib.parse
from hashlib import sha256


def get_next_name(file_path: str) -> str:
    """
    Get next available name to download file.

    Parameters
    ----------
    file_path: str
        Absolute path of the file for which next available name to
        be generated.

    Returns
    -------
    str
        Absolute path of the next available name for the file.
    """
    posix_path = pathlib.Path(file_path)
    counter: int = 1
    new_file_name: str = os.path.join("{0}", "{1}-copy{2}{3}")
    while os.path.isfile(
        new_file_name.format(
            posix_path.parent,
            posix_path.stem,
            counter,
            "".join(posix_path.suffixes),
        )
    ):
        counter += 1
    return new_file_name.format(
        posix_path.parent,
        posix_path.stem,
        counter,
        "".join(posix_path.suffixes),
    )


def _file_md5(file_path: str) -> str:
    """Compute the SHA-256 hash of a file without leaking the file descriptor."""
    hasher = sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def manage_duplicate_file(file_path: str):
    """
    Check if a file is duplicate.

    Compare the SHA-256 hash of files with copy name pattern
    and remove if the hash is same.

    Parameters
    ----------
    file_path: str
        Absolute path of the file for which duplicates needs to
        be managed.

    Returns
    -------
    str
        Absolute path of the duplicate managed file.
    """
    posix_path = pathlib.Path(file_path)
    file_base_name: str = "".join(posix_path.stem.split("-copy")[0])
    name_pattern: str = f"{posix_path.parent}/{file_base_name}*"
    # Reason for using `str.translate()`
    # https://stackoverflow.com/q/22055500/6730439
    old_files: list = glob.glob(
        name_pattern.translate({ord("["): "[[]", ord("]"): "[]]"})
    )
    if file_path in old_files:
        old_files.remove(file_path)
    current_file_md5: str = _file_md5(file_path)
    for old_file_path in old_files:
        old_file_md5: str = _file_md5(old_file_path)
        if current_file_md5 == old_file_md5:
            os.remove(file_path)
            return old_file_path
    return file_path


def to_media_url(file_path: str, base_dir: str, this_dir: str) -> str:
    """Convert an absolute file path to a ``/media/...`` URL.

    Parameters
    ----------
    file_path: str
        Absolute path to a downloaded media file.
    base_dir: str
        Configured download directory (may be empty). Falls back to
        ``this_dir``.
    this_dir: str
        Project root directory (fallback base).

    Returns
    -------
    str
        A relative ``/media/...`` URL if the file is under the base
        directory, or an empty string otherwise.
    """
    abs_fpath = os.path.abspath(file_path)
    abs_base = os.path.abspath(base_dir) if base_dir else this_dir
    if abs_fpath.startswith(abs_base):
        rel_path = os.path.relpath(abs_fpath, abs_base)
        rel_path = rel_path.replace("\\", "/")
        encoded_path = urllib.parse.quote(rel_path, safe="/")
        return f"/media/{encoded_path}"
    return ""
