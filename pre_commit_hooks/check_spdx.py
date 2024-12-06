"""This script checks for the presence of an SPDX-License-Identifier in the comments of source files."""
from __future__ import annotations

import argparse
import re
from collections.abc import Sequence


def _load_file(file_path: str) -> str:
    try:
        with open(file_path, encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading file content of {file_path}: {e}")


def _check_spdx(file_content: str) -> bool:
    for line in file_content:
        stripped_line = line.strip()
        if stripped_line.startswith('#') or stripped_line.startswith('//') or re.match(r'^\s*/\*', stripped_line):
            if 'SPDX-License-Identifier:' in stripped_line:
                return True
        else:
            break


def check_spdx(file_paths: list[str]) -> int:
    """
    Check if the given files contain an SPDX license identifier.

    Args:
        file_paths (list of str): List of file paths to check.

    Returns:
        int: Returns 0 if all files contain an SPDX license identifier,
             otherwise returns 1 if any file is missing the SPDX line.
    """
    any_missing_spdx = False
    for file_path in file_paths:
        file_content = _load_file(file_path)
        if not file_content:
            return 1

        if not _check_spdx(file_path):
            print(f"Missing SPDX line in {file_path}")
            any_missing_spdx = True

    if any_missing_spdx:
        return 1
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    return check_spdx(args.filenames)


if __name__ == '__main__':
    raise SystemExit(main())
