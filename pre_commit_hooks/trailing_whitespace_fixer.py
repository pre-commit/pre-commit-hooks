from __future__ import print_function

import argparse
import os
import sys


def _fix_file(filename, is_markdown):
    with open(filename, mode='rb') as file_processed:
        lines = file_processed.readlines()
    newlines = [_process_line(line, is_markdown) for line in lines]
    if newlines != lines:
        with open(filename, mode='wb') as file_processed:
            for line in newlines:
                file_processed.write(line)
        return True
    else:
        return False


def _process_line(line, is_markdown):
    if line[-2:] == b'\r\n':
        eol = b'\r\n'
    elif line[-1:] == b'\n':
        eol = b'\n'
    else:
        eol = b''
    # preserve trailing two-space for non-blank lines in markdown files
    if is_markdown and (not line.isspace()) and line.endswith(b'  ' + eol):
        return line.rstrip() + b'  ' + eol
    return line.rstrip() + eol


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--no-markdown-linebreak-ext',
        action='store_const',
        const=[],
        default=argparse.SUPPRESS,
        dest='markdown_linebreak_ext',
        help='Do not preserve linebreak spaces in Markdown',
    )
    parser.add_argument(
        '--markdown-linebreak-ext',
        action='append',
        const='',
        default=['md,markdown'],
        metavar='*|EXT[,EXT,...]',
        nargs='?',
        help='Markdown extensions (or *) for linebreak spaces',
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    md_args = args.markdown_linebreak_ext
    if '' in md_args:
        parser.error('--markdown-linebreak-ext requires a non-empty argument')
    all_markdown = '*' in md_args
    # normalize all extensions; split at ',', lowercase, and force 1 leading '.'
    md_exts = [
        '.' + x.lower().lstrip('.') for x in ','.join(md_args).split(',')
    ]

    # reject probable "eaten" filename as extension (skip leading '.' with [1:])
    for ext in md_exts:
        if any(c in ext[1:] for c in r'./\:'):
            parser.error(
                "bad --markdown-linebreak-ext extension '{}' (has . / \\ :)\n"
                "  (probably filename; use '--markdown-linebreak-ext=EXT')"
                .format(ext),
            )

    return_code = 0
    for filename in args.filenames:
        _, extension = os.path.splitext(filename.lower())
        md = all_markdown or extension in md_exts
        if _fix_file(filename, md):
            print('Fixing {}'.format(filename))
            return_code = 1
    return return_code


if __name__ == '__main__':
    sys.exit(main())
