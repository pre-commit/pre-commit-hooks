from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import re
import tokenize
from typing import List
from typing import Optional
from typing import Sequence

START_QUOTE_RE = re.compile('^[a-zA-Z]*"')


def handle_match(token_text):  # type: (str) -> str
    if '"""' in token_text or "'''" in token_text:
        return token_text

    match = START_QUOTE_RE.match(token_text)
    if match is not None:
        meat = token_text[match.end():-1]
        if '"' in meat or "'" in meat:
            return token_text
        else:
            return match.group().replace('"', "'") + meat + "'"
    else:
        return token_text


def get_line_offsets_by_line_no(src):  # type: (str) -> List[int]
    # Padded so we can index with line number
    offsets = [-1, 0]
    for line in src.splitlines():
        offsets.append(offsets[-1] + len(line) + 1)
    return offsets


def fix_strings(filename):  # type: (str) -> int
    with io.open(filename, encoding='UTF-8') as f:
        contents = f.read()
    line_offsets = get_line_offsets_by_line_no(contents)

    # Basically a mutable string
    splitcontents = list(contents)

    # Iterate in reverse so the offsets are always correct
    tokens = reversed(list(tokenize.generate_tokens(
        io.StringIO(contents).readline,
    )))
    for token_type, token_text, (srow, scol), (erow, ecol), _ in tokens:
        if token_type == tokenize.STRING:
            new_text = handle_match(token_text)
            splitcontents[
                line_offsets[srow] + scol:
                line_offsets[erow] + ecol
            ] = new_text

    new_contents = ''.join(splitcontents)
    if contents != new_contents:
        with io.open(filename, 'w', encoding='UTF-8') as write_handle:
            write_handle.write(new_contents)
        return 1
    else:
        return 0


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        return_value = fix_strings(filename)
        if return_value != 0:
            print('Fixing strings in {}'.format(filename))
        retv |= return_value

    return retv


if __name__ == '__main__':
    exit(main())
