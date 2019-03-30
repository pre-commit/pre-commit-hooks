from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import tokenize
from typing import Optional
from typing import Sequence

import six

if six.PY2:  # pragma: no cover (PY2)
    from tokenize import generate_tokens as tokenize_tokenize
    OTHER_NON_CODE = ()
else:  # pragma: no cover (PY3)
    from tokenize import tokenize as tokenize_tokenize
    OTHER_NON_CODE = (tokenize.ENCODING,)

NON_CODE_TOKENS = frozenset(
    (tokenize.COMMENT, tokenize.ENDMARKER, tokenize.NEWLINE, tokenize.NL) +
    OTHER_NON_CODE,
)


def check_docstring_first(src, filename='<unknown>'):
    # type: (bytes, str) -> int
    """Returns nonzero if the source has what looks like a docstring that is
    not at the beginning of the source.

    A string will be considered a docstring if it is a STRING token with a
    col offset of 0.
    """
    found_docstring_line = None
    found_code_line = None

    tok_gen = tokenize_tokenize(io.BytesIO(src).readline)
    for tok_type, _, (sline, scol), _, _ in tok_gen:
        # Looks like a docstring!
        if tok_type == tokenize.STRING and scol == 0:
            if found_docstring_line is not None:
                print(
                    '{}:{} Multiple module docstrings '
                    '(first docstring on line {}).'.format(
                        filename, sline, found_docstring_line,
                    ),
                )
                return 1
            elif found_code_line is not None:
                print(
                    '{}:{} Module docstring appears after code '
                    '(code seen on line {}).'.format(
                        filename, sline, found_code_line,
                    ),
                )
                return 1
            else:
                found_docstring_line = sline
        elif tok_type not in NON_CODE_TOKENS and found_code_line is None:
            found_code_line = sline

    return 0


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        with open(filename, 'rb') as f:
            contents = f.read()
        retv |= check_docstring_first(contents, filename=filename)

    return retv
