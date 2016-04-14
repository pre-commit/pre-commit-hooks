from __future__ import print_function

import argparse
import sys
from collections import OrderedDict

import simplejson


def _get_pretty_format(contents, indent, sort_keys=True):
    return simplejson.dumps(
        simplejson.loads(
            contents,
            object_pairs_hook=None if sort_keys else OrderedDict,
        ),
        sort_keys=sort_keys,
        indent=indent
    ) + "\n"  # dumps don't end with a newline


def _autofix(filename, new_contents):
    print("Fixing file {0}".format(filename))
    with open(filename, 'w') as f:
        f.write(new_contents)


def pretty_format_json(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--autofix',
        action='store_true',
        dest='autofix',
        help='Automatically fixes encountered not-pretty-formatted files',
    )
    parser.add_argument(
        '--indent',
        type=int,
        default=2,
        help='Number of indent spaces used to pretty-format files',
    )
    parser.add_argument(
        '--no-sort-keys',
        action='store_true',
        dest='no_sort_keys',
        default=False,
        help='Keep JSON nodes in the same order',
    )

    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    status = 0

    for json_file in args.filenames:
        with open(json_file) as f:
            contents = f.read()

        try:
            pretty_contents = _get_pretty_format(
                contents, args.indent, sort_keys=not args.no_sort_keys,
            )

            if contents != pretty_contents:
                print("File {0} is not pretty-formatted".format(json_file))

                if args.autofix:
                    _autofix(json_file, pretty_contents)

                status = 1

        except simplejson.JSONDecodeError:
            print(
                "Input File {0} is not a valid JSON, consider using check-json"
                .format(json_file)
            )
            return 1

    return status


if __name__ == '__main__':
    sys.exit(pretty_format_json())
