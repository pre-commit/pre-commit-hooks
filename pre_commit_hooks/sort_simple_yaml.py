"""Sort a simple YAML file, keeping blocks of comments and definitions
together.

We assume a strict subset of YAML that looks like:

    # block of header comments
    # here that should always
    # be at the top of the file

    # optional comments
    # can go here
    key: value
    key: value

    key: value

In other words, we don't sort deeper than the top layer, and might corrupt
complicated YAML files.
"""
from __future__ import annotations

import argparse
from typing import Sequence


QUOTES = ["'", '"']


def sort(lines: list[str]) -> list[str]:
    """Sort a YAML file in alphabetical order, keeping blocks together.

    :param lines: array of strings (without newlines)
    :return: sorted array of strings
    """
    # make a copy of lines since we will clobber it
    lines = list(lines)
    new_lines = parse_block(lines, header=True)

    for block in sorted(parse_blocks(lines), key=first_key):
        if new_lines:
            new_lines.append('')
        new_lines.extend(block)

    return new_lines


def parse_block(lines: list[str], header: bool = False) -> list[str]:
    """Parse and return a single block, popping off the start of `lines`.

    If parsing a header block, we stop after we reach a line that is not a
    comment. Otherwise, we stop after reaching an empty line.

    :param lines: list of lines
    :param header: whether we are parsing a header block
    :return: list of lines that form the single block
    """
    block_lines = []
    while lines and lines[0] and (not header or lines[0].startswith('#')):
        block_lines.append(lines.pop(0))
    return block_lines


def parse_blocks(lines: list[str]) -> list[list[str]]:
    """Parse and return all possible blocks, popping off the start of `lines`.

    :param lines: list of lines
    :return: list of blocks, where each block is a list of lines
    """
    blocks = []

    while lines:
        if lines[0] == '':
            lines.pop(0)
        else:
            blocks.append(parse_block(lines))

    return blocks


def first_key(lines: list[str]) -> str:
    """Returns a string representing the sort key of a block.

    The sort key is the first YAML key we encounter, ignoring comments, and
    stripping leading quotes.

    >>> print(test)
    # some comment
    'foo': true
    >>> first_key(test)
    'foo'
    """
    for line in lines:
        if line.startswith('#'):
            continue
        if any(line.startswith(quote) for quote in QUOTES):
            return line[1:]
        return line
    else:
        return ''  # not actually reached in reality


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retval = 0

    for filename in args.filenames:
        with open(filename, 'r+') as f:
            lines = [line.rstrip() for line in f.readlines()]
            new_lines = sort(lines)

            if lines != new_lines:
                print(f'Fixing file `{filename}`')
                f.seek(0)
                f.write('\n'.join(new_lines) + '\n')
                f.truncate()
                retval = 1

    return retval


if __name__ == '__main__':
    raise SystemExit(main())
