from __future__ import annotations

import argparse
import json
import re
from typing import Any, Sequence


def raise_duplicate_keys(
        ordered_pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    d = {}
    for key, val in ordered_pairs:
        if key in d:
            raise ValueError(f'Duplicate key: {key}')
        else:
            d[key] = val
    return d

def check_mixed_indentation(content: str, filename: str) -> bool:
    """
    Checks a string content for mixed indentation (tabs and spaces) in leading whitespace.

    Args:
        content (str): The content of the file to check.
        filename (str): The name of the file being checked (for reporting purposes).

    Returns:
        bool: True if mixed indentation is found, False otherwise.
    """
    found_mixed = False

    for i, line in enumerate(content.splitlines(), 1):
        # Determine leading whitespace
        leading_whitespace = line[:len(line) - len(line.lstrip())]

        # Check if both tabs and spaces are present in leading whitespace
        if ' ' in leading_whitespace and '\t' in leading_whitespace:
            print(f"{filename}: Mixed indentation (tabs and spaces) found on line {i}")
            found_mixed = True

    return not found_mixed

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        with open(filename, 'r') as f:
            content = f.read()

        # Check for mixed indentation first
        if not check_mixed_indentation(content, filename):
            retval = 1
            continue

        # Then, attempt to parse the JSON
        try:
            json.loads(content, object_pairs_hook=raise_duplicate_keys)
        except ValueError as exc:
            print(f'{filename}: Failed to json decode ({exc})')
            retval = 1

    return retval


if __name__ == '__main__':
    raise SystemExit(main())
