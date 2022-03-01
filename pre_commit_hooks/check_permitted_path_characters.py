from __future__ import annotations

import argparse
import string
from typing import Sequence

DEFAULT_ALLOWLIST = string.ascii_letters + string.digits + '-_./'


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument(
        '--allowlist',
        default=DEFAULT_ALLOWLIST,
        help=(
            'Override the default allowlist of permitted characters. The'
            ' default is %(default)s'
        ),
    )
    parser.add_argument(
        '--extra-allowlist',
        default='',
        help='Extend the default allowlist with these characters.',
    )
    args = parser.parse_args(argv)

    allowlist = set(args.allowlist + args.extra_allowlist)

    retcode = 0
    for filename in args.filenames:
        # check the entire path, not just the filename, to catch directories
        # with invalid characters
        file_chars = set(filename)
        if not file_chars.issubset(allowlist):
            # sorted and stringified for readability
            pretty_allowlist = ''.join(sorted(allowlist))
            pretty_banlist = repr(''.join(sorted(file_chars - allowlist)))
            print(
                f'"{filename}" contains characters not in the allowlist:'
                f' "{pretty_banlist}". Allowlist is: "{pretty_allowlist}".',
            )
            retcode = 1

    return retcode


if __name__ == '__main__':
    raise SystemExit(main())
