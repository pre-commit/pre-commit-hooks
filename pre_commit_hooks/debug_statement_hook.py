from __future__ import annotations

import argparse
import ast
import traceback
from typing import NamedTuple
from typing import Sequence


DEBUG_STATEMENTS = {
    'bpdb',
    'ipdb',
    'pdb',
    'pdbr',
    'pudb',
    'pydevd_pycharm',
    'q',
    'rdb',
    'rpdb',
    'wdb',
}


class Debug(NamedTuple):
    line: int
    col: int
    name: str
    reason: str


class DebugStatementParser(ast.NodeVisitor):
    def __init__(self) -> None:
        self.breakpoints: list[Debug] = []

    def visit_Import(self, node: ast.Import) -> None:
        for name in node.names:
            if name.name in DEBUG_STATEMENTS:
                st = Debug(node.lineno, node.col_offset, name.name, 'imported')
                self.breakpoints.append(st)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module in DEBUG_STATEMENTS:
            st = Debug(node.lineno, node.col_offset, node.module, 'imported')
            self.breakpoints.append(st)

    def visit_Call(self, node: ast.Call) -> None:
        """python3.7+ breakpoint()"""
        if isinstance(node.func, ast.Name) and node.func.id == 'breakpoint':
            st = Debug(node.lineno, node.col_offset, node.func.id, 'called')
            self.breakpoints.append(st)
        self.generic_visit(node)


def check_file(filename: str) -> int:
    try:
        with open(filename, 'rb') as f:
            ast_obj = ast.parse(f.read(), filename=filename)
    except SyntaxError:
        print(f'{filename} - Could not parse ast')
        print()
        print('\t' + traceback.format_exc().replace('\n', '\n\t'))
        print()
        return 1

    visitor = DebugStatementParser()
    visitor.visit(ast_obj)

    for bp in visitor.breakpoints:
        print(f'{filename}:{bp.line}:{bp.col}: {bp.name} {bp.reason}')

    return int(bool(visitor.breakpoints))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    args = parser.parse_args(argv)

    retv = 0
    for filename in args.filenames:
        retv |= check_file(filename)
    return retv


if __name__ == '__main__':
    raise SystemExit(main())
