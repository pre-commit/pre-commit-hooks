from __future__ import annotations

import argparse
import ast
from collections.abc import Sequence
from typing import NamedTuple


BUILTIN_TYPES = {
    'complex': '0j',
    'dict': '{}',
    'float': '0.0',
    'int': '0',
    'list': '[]',
    'str': "''",
    'tuple': '()',
}


class Call(NamedTuple):
    name: str
    line: int
    column: int


class Visitor(ast.NodeVisitor):
    def __init__(
            self,
            ignore: set[str],
            allow_dict_kwargs: bool = True,
    ) -> None:
        self.builtin_type_calls: list[Call] = []
        self.allow_dict_kwargs = allow_dict_kwargs
        self._disallowed = BUILTIN_TYPES.keys() - ignore

    def _check_dict_call(self, node: ast.Call) -> bool:
        return self.allow_dict_kwargs and bool(node.keywords)

    def visit_Call(self, node: ast.Call) -> None:
        if (
            # Ignore functions that are object attributes (`foo.bar()`).
            # Assume that if the user calls `builtins.list()`, they know what
            # they're doing.
            isinstance(node.func, ast.Name) and
            node.func.id in self._disallowed and
            (node.func.id != 'dict' or not self._check_dict_call(node)) and
            not node.args
        ):
            self.builtin_type_calls.append(
                Call(node.func.id, node.lineno, node.col_offset),
            )

        self.generic_visit(node)


def check_file(
        filename: str,
        *,
        ignore: set[str],
        allow_dict_kwargs: bool = True,
) -> list[Call]:
    with open(filename, 'rb') as f:
        tree = ast.parse(f.read(), filename=filename)
    visitor = Visitor(ignore=ignore, allow_dict_kwargs=allow_dict_kwargs)
    visitor.visit(tree)
    return visitor.builtin_type_calls


def parse_ignore(value: str) -> set[str]:
    return set(value.split(','))


def main(argv: Sequence[str] | None = None) -> int:
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
                f'{filename}:{call.line}:{call.column}: '
                f'replace {call.name}() with {BUILTIN_TYPES[call.name]}',
            )
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
