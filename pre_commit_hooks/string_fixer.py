from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re
import tokenize


double_quote_starts = tuple(s for s in tokenize.single_quoted if '"' in s)
compiled_tokenize_string = re.compile('(?<!")' + tokenize.String + '(?!")')


def handle_match(m):
    string = m.group(0)

    for double_quote_start in double_quote_starts:
        if string.startswith(double_quote_start):
            meat = string[len(double_quote_start):-1]
            if '"' in meat or "'" in meat:
                break
            return double_quote_start.replace('"', "'") + meat + "'"
    return string


def fix_strings(filename):
    contents = open(filename).read()
    new_contents = compiled_tokenize_string.sub(handle_match, contents)
    retval = int(new_contents != contents)
    if retval:
        with open(filename, 'w') as write_handle:
            write_handle.write(new_contents)
    return retval


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
