from __future__ import print_function

import argparse
import io
import sys
from collections import OrderedDict

import simplejson
import six


def _get_pretty_format(contents, indent, ensure_ascii=True, sort_keys=True, top_keys=[]):
    def pairs_first(pairs):
        before = [pair for pair in pairs if pair[0] in top_keys]
        before = sorted(before, key=lambda x: top_keys.index(x[0]))
        after = [pair for pair in pairs if pair[0] not in top_keys]
        if sort_keys:
            after = sorted(after, key=lambda x: x[0])
        return OrderedDict(before + after)
    return six.text_type(simplejson.dumps(
        simplejson.loads(
            contents,
            object_pairs_hook=pairs_first,
        ),
        indent=indent,
        ensure_ascii=ensure_ascii,
    )) + "\n"  # dumps does not end with a newline


def _autofix(filename, new_contents):
    print("Fixing file {}".format(filename))
    with io.open(filename, 'w', encoding='UTF-8') as f:
        f.write(new_contents)


def parse_indent(s):
    # type: (str) -> str
    try:
        int_indentation_spec = int(s)
    except ValueError:
        if not s.strip():
            return s
        else:
            raise ValueError(
                'Non-whitespace JSON indentation delimiter supplied. ',
            )
    else:
        if int_indentation_spec >= 0:
            return int_indentation_spec * ' '
        else:
            raise ValueError(
                'Negative integer supplied to construct JSON indentation delimiter. ',
            )


def parse_topkeys(s):
    # type: (str) -> array
    return s.split(',')


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
        type=parse_indent,
        default='  ',
        help='String used as delimiter for one indentation level',
    )
    parser.add_argument(
        '--no-ensure-ascii',
        action='store_true',
        dest='no_ensure_ascii',
        default=False,
        help='Do NOT convert non-ASCII characters to Unicode escape sequences (\\uXXXX)',
    )
    parser.add_argument(
        '--no-sort-keys',
        action='store_true',
        dest='no_sort_keys',
        default=False,
        help='Keep JSON nodes in the same order',
    )
    parser.add_argument(
        '--top-keys',
        type=parse_topkeys,
        dest='top_keys',
        default=[],
        help='Ordered list of keys to keep at the top of JSON hashes',
    )

    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    status = 0

    for json_file in args.filenames:
        with io.open(json_file, encoding='UTF-8') as f:
            contents = f.read()

        try:
            pretty_contents = _get_pretty_format(
                contents, args.indent, ensure_ascii=not args.no_ensure_ascii,
                sort_keys=not args.no_sort_keys, top_keys=args.top_keys,
            )

            if contents != pretty_contents:
                print("File {} is not pretty-formatted".format(json_file))

                if args.autofix:
                    _autofix(json_file, pretty_contents)

                status = 1

        except simplejson.JSONDecodeError:
            print(
                "Input File {} is not a valid JSON, consider using check-json"
                .format(json_file),
            )
            return 1

    return status


if __name__ == '__main__':
    sys.exit(pretty_format_json())
