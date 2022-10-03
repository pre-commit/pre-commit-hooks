from __future__ import annotations

import argparse
import ast
import io
import tokenize
from tokenize import tokenize as tokenize_tokenize
from typing import Sequence

NON_CODE_TOKENS = frozenset((
    tokenize.COMMENT, tokenize.ENDMARKER, tokenize.NEWLINE, tokenize.NL,
    tokenize.ENCODING,
))


def _push_code(seen_code: io.StringIO, tok_type: int, text: str):
    if tok_type == tokenize.ENCODING:
        return
    seen_code.write(text)
    if text and not text.isspace():
        seen_code.write(' ')


def check_docstring_first(src: bytes, filename: str = '<unknown>') -> int:
    """Returns nonzero if the source has what looks like a docstring that is
    not at the beginning of the source.

    A string will be considered a docstring if it is a STRING token with a
    col offset of 0.
    """
    found_docstring_line = None
    found_code_line = None
    seen_code = io.StringIO()

    tok_gen = tokenize_tokenize(io.BytesIO(src).readline)
    for tok_type, _, (sline, scol), _, _ in tok_gen:
        # Looks like a docstring!
        if tok_type == tokenize.STRING and scol == 0:
            if found_docstring_line is not None:
                tree = ast.parse(seen_code.getvalue())
                assignments = ast.AnnAssign, ast.Assign, ast.AugAssign
                if tree.body and isinstance(tree.body[-1], assignments):
                    return 0

                print(
                    f'{filename}:{sline}: Multiple module docstrings '
                    f'(first docstring on line {found_docstring_line}).',
                )
                return 1
            elif found_code_line is not None:
                print(
                    f'{filename}:{sline}: Module docstring appears after code '
                    f'(code seen on line {found_code_line}).',
                )
                return 1
            else:
                found_docstring_line = sline
        elif tok_type not in NON_CODE_TOKENS and found_code_line is None:
            _push_code(seen_code, tok_type, text)
            found_code_line = sline
        else:
            _push_code(seen_code, tok_type, text)

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        with open(filename, 'rb') as f:
            contents = f.read()
        retv |= check_docstring_first(contents, filename=filename)

    return retv
