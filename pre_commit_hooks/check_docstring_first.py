import argparse
import io
import tokenize
from tokenize import tokenize as tokenize_tokenize
from typing import Optional
from typing import Sequence

NON_CODE_TOKENS = frozenset((
    tokenize.COMMENT, tokenize.ENDMARKER, tokenize.NEWLINE, tokenize.NL,
    tokenize.ENCODING,
))


def check_docstring_first(src: bytes, filename: str) -> int:
    """Returns nonzero if the source has what looks like a docstring that is
    not at the beginning of the source.

    A string will be considered a docstring if it is a STRING token with a
    col offset of 0.
    """
    found_docstring_line = None
    found_code_line = None
    assignment_lines = set()

    tok_gen = tokenize_tokenize(io.BytesIO(src).readline)
    for tok_type, string, (sline, scol), _, _ in tok_gen:
        # Save all lines with top-level attribute assignments
        if scol == 2 and tok_type == tokenize.OP and string == '=':
            assignment_lines.add(sline)

        # Looks like a docstring!
        if tok_type == tokenize.STRING and scol == 0:
            if found_docstring_line is not None:
                print(
                    f'{filename}:{sline} Multiple module docstrings '
                    f'(first docstring on line {found_docstring_line}).',
                )
                return 1
            elif (
                    found_code_line is not None and
                    sline > 0 and sline - 1 not in assignment_lines
            ):
                print(
                    f'{filename}:{sline} Module docstring appears after code '
                    f'(code seen on line {found_code_line}).',
                )
                return 1
            else:
                found_docstring_line = sline
        elif tok_type not in NON_CODE_TOKENS and found_code_line is None:
            found_code_line = sline

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        with open(filename, 'rb') as f:
            contents = f.read()
        retv |= check_docstring_first(contents, filename)

    return retv
