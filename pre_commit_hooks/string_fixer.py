from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re
import tokenize


double_quote_starts = tuple(s for s in tokenize.single_quoted if '"' in s)
compiled_tokenize_string = re.compile(tokenize.String)


def handle_match(m):
    string = m.group(0)

    for double_quote_start in double_quote_starts:
        if string.startswith(double_quote_start):
            meat = string[len(double_quote_start):-1]
            if '"' in meat or "'" in meat:
                break
            return (
                double_quote_start.replace('"', "'") +
                string[len(double_quote_start):-1] +
                "'"
            )
    return string


def fix_strings(filename):
    return_value = 0

    lines = []

    with open(filename, 'r') as read_handle:
        for line in read_handle:
            if '"""' in line:
                # Docstrings are hard, fuck it
                lines.append(line)
            else:
                result = re.sub(compiled_tokenize_string, handle_match, line)
                lines.append(result)
                return_value |= int(result != line)

    with open(filename, 'w') as write_handle:
        for line in lines:
            write_handle.write(line)

    return return_value


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
