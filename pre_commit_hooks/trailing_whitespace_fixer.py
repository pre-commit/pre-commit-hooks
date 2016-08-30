from __future__ import print_function

import argparse
import os
import sys
import tempfile

from pre_commit_hooks.util import cmd_output


def _fix_file(filename, markdown=False):
    with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as tmp_file:
        with open(filename, mode='rb') as original_file:
            for line in original_file.readlines():
                # preserve trailing two-space for non-blank lines in markdown files
                eol = b'\r\n' if line[-2:] == b'\r\n' else b'\n'
                if markdown and (not line.isspace()) and line.endswith(b'  ' + eol):
                    line = line.rstrip(b' \r\n')  # restricted stripping: e.g. \t are not stripped
                    # only preserve if there are no trailing tabs or unusual whitespace
                    if not line[-1:].isspace():
                        tmp_file.write(line + b'  ' + eol)
                        continue
                tmp_file.write(line.rstrip() + eol)
    os.remove(filename)
    os.rename(tmp_file.name, filename)


def fix_trailing_whitespace(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--no-markdown-linebreak-ext',
        action='store_const',
        const=[],
        default=argparse.SUPPRESS,
        dest='markdown_linebreak_ext',
        help='Do not preserve linebreak spaces in Markdown'
    )
    parser.add_argument(
        '--markdown-linebreak-ext',
        action='append',
        const='',
        default=['md,markdown'],
        metavar='*|EXT[,EXT,...]',
        nargs='?',
        help='Markdown extensions (or *) for linebreak spaces'
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    bad_whitespace_files = cmd_output(
        'grep', '-l', '[[:space:]]$', *args.filenames, retcode=None
    ).strip().splitlines()

    md_args = args.markdown_linebreak_ext
    if '' in md_args:
        parser.error('--markdown-linebreak-ext requires a non-empty argument')
    all_markdown = '*' in md_args
    # normalize all extensions; split at ',', lowercase, and force 1 leading '.'
    md_exts = ['.' + x.lower().lstrip('.')
               for x in ','.join(md_args).split(',')]

    # reject probable "eaten" filename as extension (skip leading '.' with [1:])
    for ext in md_exts:
        if any(c in ext[1:] for c in r'./\:'):
            parser.error(
                "bad --markdown-linebreak-ext extension '{0}' (has . / \\ :)\n"
                "  (probably filename; use '--markdown-linebreak-ext=EXT')"
                .format(ext)
            )

    return_code = 0
    for bad_whitespace_file in bad_whitespace_files:
        print('Fixing {0}'.format(bad_whitespace_file))
        _, extension = os.path.splitext(bad_whitespace_file.lower())
        _fix_file(bad_whitespace_file, all_markdown or extension in md_exts)
        return_code = 1
    return return_code


if __name__ == '__main__':
    sys.exit(fix_trailing_whitespace())
