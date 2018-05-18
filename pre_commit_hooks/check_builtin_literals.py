from __future__ import unicode_literals

import argparse
import ast
import collections
import sys


BUILTIN_TYPES = {
    'complex': '0j',
    'dict': '{}',
    'float': '0.0',
    'int': '0',
    'list': '[]',
    'str': "''",
    'tuple': '()',
}


BuiltinTypeCall = collections.namedtuple('BuiltinTypeCall', ['name', 'line', 'column'])


class BuiltinTypeVisitor(ast.NodeVisitor):
    def __init__(self, ignore=None, allow_dict_kwargs=True):
        self.builtin_type_calls = []
        self.ignore = set(ignore) if ignore else set()
        self.allow_dict_kwargs = allow_dict_kwargs

    def _check_dict_call(self, node):
        return self.allow_dict_kwargs and (getattr(node, 'kwargs', None) or getattr(node, 'keywords', None))

    def visit_Call(self, node):
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
            BuiltinTypeCall(node.func.id, node.lineno, node.col_offset),
        )


def check_file_for_builtin_type_constructors(filename, ignore=None, allow_dict_kwargs=True):
    tree = ast.parse(open(filename, 'rb').read(), filename=filename)
    visitor = BuiltinTypeVisitor(ignore=ignore, allow_dict_kwargs=allow_dict_kwargs)
    visitor.visit(tree)
    return visitor.builtin_type_calls


def parse_args(argv):
    def parse_ignore(value):
        return set(value.split(','))

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('--ignore', type=parse_ignore, default=set())

    allow_dict_kwargs = parser.add_mutually_exclusive_group(required=False)
    allow_dict_kwargs.add_argument('--allow-dict-kwargs', action='store_true')
    allow_dict_kwargs.add_argument('--no-allow-dict-kwargs', dest='allow_dict_kwargs', action='store_false')
    allow_dict_kwargs.set_defaults(allow_dict_kwargs=True)

    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    rc = 0
    for filename in args.filenames:
        calls = check_file_for_builtin_type_constructors(
            filename,
            ignore=args.ignore,
            allow_dict_kwargs=args.allow_dict_kwargs,
        )
        if calls:
            rc = rc or 1
        for call in calls:
            print(
                '{filename}:{call.line}:{call.column} - Replace {call.name}() with {replacement}'.format(
                    filename=filename,
                    call=call,
                    replacement=BUILTIN_TYPES[call.name],
                ),
            )
    return rc


if __name__ == '__main__':
    sys.exit(main())
