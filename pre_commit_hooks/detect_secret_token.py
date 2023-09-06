from __future__ import annotations

import argparse
import re
import sys
from typing import Sequence

# secret token is defined in https://datatracker.ietf.org/doc/html/rfc8959 as:
#
# secret-token-URI    = secret-token-scheme ":" token
# secret-token-scheme = "secret-token"
# token               = 1*pchar
#
# pchar is defined in https://www.rfc-editor.org/rfc/rfc3986#section-3.3 as:
#
# pchar         = unreserved / pct-encoded / sub-delims / ":" / "@"
SECRET_TOKEN_RE = re.compile(
    'secret-token:('
    r"[A-Za-z0-9\-._~!$&'()*+,;=:@]"  # unreserved / sub-delims / ":" / "@"
    '|%[0-9A-Fa-f]{2}'  # pct-encoded
    ')+',
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    found = False
    for filename in args.filenames:
        with open(filename) as f:
            if SECRET_TOKEN_RE.match(f.read()):
                found = True
                print(f'secret-token found: {filename}', file=sys.stderr)

    return int(found)


if __name__ == '__main__':
    raise SystemExit(main())
