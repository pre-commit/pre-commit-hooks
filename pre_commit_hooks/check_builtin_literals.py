from __future__ import unicode_literals

import argparse
import ast
import collections
import sys
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set


BUILTIN_TYPES = {
    'complex': '0j',
    'dict': '{}',
    'float': '0.0',
    'int': '0',
    'list': '[]',
    'str': "''",
    'tuple': '()',
}


Call = collections.namedtuple('Call', ['name', 'line', 'column'])


class Visitor(ast.NodeVisitor):
    def __init__(self, ignore=None, allow_dict_kwargs=True):
        # type: (Optional[Sequence[str]], bool) -> None
        self.builtin_type_calls = []  # type: List[Call]
        self.ignore = set(ignore) if ignore else set()
        self.allow_dict_kwargs = allow_dict_kwargs

    def _check_dict_call(self, node):  # type: (ast.Call) -> bool
        return (
            self.allow_dict_kwargs and
            (getattr(node, 'kwargs', None) or getattr(node, 'keywords', None))
        )

    def visit_Call(self, node):  # type: (ast.Call) -> None
        if not isinstance(node.func, ast.Name):
            # Ignore functions that are object attributes (`foo.bar()`).
            # Assume that if the user calls `builtins.list()`, they know what
            # they're doing.
            return
        if node.func.id not in set(BUILTIN_TYPES).difference(self.ignore):
            return
        if node.func.id == 'dict' and self._check_dict_call(node):
            return
        elif node.args:
            return
        self.builtin_type_calls.append(
            Call(node.func.id, node.lineno, node.col_offset),
        )


def check_file(filename, ignore=None, allow_dict_kwargs=True):
    # type: (str, Optional[Sequence[str]], bool) -> List[Call]
    with open(filename, 'rb') as f:
        tree = ast.parse(f.read(), filename=filename)
    visitor = Visitor(ignore=ignore, allow_dict_kwargs=allow_dict_kwargs)
    visitor.visit(tree)
    return visitor.builtin_type_calls


def parse_ignore(value):  # type: (str) -> Set[str]
    return set(value.split(','))


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('--ignore', type=parse_ignore, default=set())

    mutex = parser.add_mutually_exclusive_group(required=False)
    mutex.add_argument('--allow-dict-kwargs', action='store_true')
    mutex.add_argument(
        '--no-allow-dict-kwargs',
        dest='allow_dict_kwargs', action='store_false',
    )
    mutex.set_defaults(allow_dict_kwargs=True)

    args = parser.parse_args(argv)

    rc = 0
    for filename in args.filenames:
        calls = check_file(
            filename,
            ignore=args.ignore,
            allow_dict_kwargs=args.allow_dict_kwargs,
        )
        if calls:
            rc = rc or 1
        for call in calls:
            print(
                '{filename}:{call.line}:{call.column}: '
                'replace {call.name}() with {replacement}'.format(
                    filename=filename,
                    call=call,
                    replacement=BUILTIN_TYPES[call.name],
                ),
            )
    return rc


if __name__ == '__main__':
    sys.exit(main())
