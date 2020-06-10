import argparse
import os
from typing import Optional
from typing import Sequence
import re


def check_for_no_commit_tokens(
        filename: str,
        tokens: Optional[Sequence[str]],
) -> str:
    with open(filename, mode='r', encoding='utf-8') as file_processed:
        lines = file_processed.read()
        for token in tokens:
            match = re.search(token, lines)
            if match:
                # no-commit token is present
                return match.string
    return None


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--tokens',
        help=(
            'The set of tokens, separated by space, used to block commits  '
            'if present. For example, "nocommit NOCOMMIT"'
        ),
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    return_code = 0
    tokens = args.tokens or ["nocommit"]

    for filename in args.filenames:
        _, extension = os.path.splitext(filename.lower())
        match_string = check_for_no_commit_tokens(filename, tokens)
        if match_string:
            print(f'Found no-commit token in {filename}: {match_string}')
            return_code = 1
    return return_code


if __name__ == '__main__':
    exit(main())
