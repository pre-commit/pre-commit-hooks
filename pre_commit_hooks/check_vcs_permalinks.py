from __future__ import annotations

import argparse
import re
import sys
from typing import Pattern
from typing import Sequence


def _get_pattern(domain: str) -> Pattern[bytes]:
    regex = (
        rf'https://{domain}/[^/ ]+/[^/ ]+/blob/'
        r'(?![a-fA-F0-9]{4,64}/)([^/. ]+)/[^# ]+#L\d+'
    )
    return re.compile(regex.encode())


def _check_filename(filename: str, patterns: list[Pattern[bytes]]) -> int:
    retv = 0
    with open(filename, 'rb') as f:
        for i, line in enumerate(f, 1):
            for pattern in patterns:
                if pattern.search(line):
                    sys.stdout.write(f'{filename}:{i}:')
                    sys.stdout.flush()
                    sys.stdout.buffer.write(line)
                    retv = 1
    return retv


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument(
        '--additional-github-domain',
        dest='additional_github_domains',
        action='append',
        default=['github.com'],
    )
    args = parser.parse_args(argv)

    patterns = [
        _get_pattern(domain)
        for domain in args.additional_github_domains
    ]

    retv = 0

    for filename in args.filenames:
        retv |= _check_filename(filename, patterns)

    if retv:
        print()
        print('Non-permanent github link detected.')
        print('On any page on github press [y] to load a permalink.')
    return retv


if __name__ == '__main__':
    raise SystemExit(main())
