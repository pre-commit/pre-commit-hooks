from __future__ import annotations

import argparse
import re
import subprocess
from collections.abc import Sequence
from pathlib import Path


# -------------------------
# Default secret patterns
# -------------------------

DEFAULT_PATTERNS: dict[str, str] = {
    # GitLab
    "gitlab_pat": r"glpat-[0-9A-Za-z_-]{20,}",
    "gitlab_runner_token": r"glrt-[0-9A-Za-z_-]{20,}",

    # GitHub
    "github_pat": r"ghp_[0-9A-Za-z]{36}",
    "github_fine_grained_pat": r"github_pat_[0-9A-Za-z_]{82}",

    # AWS
    "aws_access_key": r"AKIA[0-9A-Z]{16}",
    "aws_secret_key": r"(?i)aws(.{0,20})?(secret|access)[-_ ]?key(.{0,20})?['\"][0-9a-zA-Z/+]{40}['\"]",

    # Generic
    "generic_secret": r"(?i)(password|passwd|pwd|secret|token|api[_-]?key)\s*=\s*['\"].+['\"]",
}



def load_custom_patterns(path: Path) -> dict[str, str]:
    patterns: dict[str, str] = {}
    for i, line in enumerate(path.read_text().splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        patterns[f"custom_rule_{i}"] = line
    return patterns


def is_binary(data: bytes) -> bool:
    return b"\x00" in data


def git_tracked_files() -> list[Path]:
    """Return all git-tracked files in the repo."""
    result = subprocess.run(
        ["git", "ls-files"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    return [Path(p) for p in result.stdout.splitlines() if p]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect exposed secrets in repository")
    parser.add_argument(
        "--rules",
        type=Path,
        help="File containing custom regex rules (one per line)",
    )
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Files to scan (if empty, scans entire repo)",
    )

    args = parser.parse_args(argv)

    patterns = dict(DEFAULT_PATTERNS)

    if args.rules:
        if not args.rules.is_file():
            print(f"Rules file not found: {args.rules}")
            return 2
        patterns.update(load_custom_patterns(args.rules))

    compiled = {
        name: re.compile(regex)
        for name, regex in patterns.items()
    }

    files: list[Path]
    if args.filenames:
        files = [Path(f) for f in args.filenames]
    else:
        files = git_tracked_files()

    findings: list[tuple[Path, str]] = []

    for path in files:
        if not path.is_file():
            continue

        try:
            data = path.read_bytes()
        except OSError:
            continue

        if is_binary(data):
            continue

        text = data.decode(errors="ignore")

        for rule, regex in compiled.items():
            if regex.search(text):
                findings.append((path, rule))

    if findings:
        print("Potential secrets detected:")
        for path, rule in findings:
            print(f"  - {path} (matched: {rule})")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
