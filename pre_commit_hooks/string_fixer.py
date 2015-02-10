from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import tokenize


double_quote_starts = tuple(s for s in tokenize.single_quoted if '"' in s)


def handle_match(token_text):
    if '"""' in token_text or "'''" in token_text:
        return token_text

    for double_quote_start in double_quote_starts:
        if token_text.startswith(double_quote_start):
            meat = token_text[len(double_quote_start):-1]
            if '"' in meat or "'" in meat:
                break
            return double_quote_start.replace('"', "'") + meat + "'"
    return token_text


def get_line_offsets_by_line_no(src):
    # Padded so we can index with line number
    offsets = [None, 0]
    for line in src.splitlines():
        offsets.append(offsets[-1] + len(line) + 1)
    return offsets


def fix_strings(filename):
    contents = io.open(filename).read()
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
        with io.open(filename, 'w') as write_handle:
            write_handle.write(new_contents)
        return 1
    else:
        return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        return_value = fix_strings(filename)
        if return_value != 0:
            print('Fixing strings in {0}'.format(filename))
        retv |= return_value

    return retv
