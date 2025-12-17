#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

FORBIDDEN = {"a", "an", "the"}


def git_ls_python_files():
    result = subprocess.run(
        ["git", "ls-files", "*.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [Path(p) for p in result.stdout.splitlines()]


def is_test_file(path: Path) -> bool:
    name = path.name
    return (
        name.startswith("test_")
        or name.startswith("tests_")
        or name.endswith("_test.py")
    )


def has_forbidden_article(path: Path) -> bool:
    parts = path.stem.split("_")
    return any(part in FORBIDDEN for part in parts)


def main() -> int:
    for path in git_ls_python_files():
        if not is_test_file(path):
            continue

        if has_forbidden_article(path):
            print("ERROR: Forbidden article in test filename:")
            print(path)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
