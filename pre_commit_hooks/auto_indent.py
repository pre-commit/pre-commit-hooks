# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import argparse
import ast
import io
import re
import textwrap
import traceback
from operator import itemgetter


RETURN_CODE = dict(
    no_change=0,
    fixed_file=1,
    syntax_error=2,
)


class IndentNodeVisitor(ast.NodeVisitor):

    def __init__(self):
        self.lines = []

    def visit_Call(self, node):
        args = list(node.args)

        if node.keywords:
            args.extend([keyword.value for keyword in node.keywords])

        if node.starargs:
            args.append(node.starargs)

        if node.kwargs:
            args.append(node.kwargs)

        try:
            if args and args[0].lineno == node.lineno:
                for arg in args:
                    if arg.lineno != node.lineno:
                        self.lines.append({
                            'line': node.lineno,
                            'nextline': arg.lineno,
                            'column': args[0].col_offset,
                        })
                        break
        except AttributeError:
            # Python 3.3 is not supported because line numbers were
            # removed from arg objects (compared to Python 2.7 and Python 3.4):
            # https://docs.python.org/3.3/library/ast.html
            pass
        finally:
            self.generic_visit(node)

    def visit_ClassDef(self, node):
        if node.bases and node.bases[0].lineno != node.lineno:
            self.generic_visit(node)
            return

        for base in node.bases:
            if base.lineno != node.lineno:
                self.lines.append({
                    'line': node.lineno,
                    'nextline': base.lineno,
                    'column': node.bases[0].col_offset,
                })

                break

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        try:
            if node.args.args and node.args.args[0].lineno != node.lineno:
                self.generic_visit(node)
                return

            for arg in node.args.args:
                if arg.lineno != node.lineno:
                    self.lines.append({
                        'line': node.lineno,
                        'nextline': arg.lineno,
                        'column': node.args.args[0].col_offset,
                    })

                    break
        except AttributeError:
            # Python 3.3 is not supported because line numbers were
            # removed from arg objects (compared to Python 2.7 and Python 3.4):
            # https://docs.python.org/3.3/library/ast.html
            pass
        finally:
            self.generic_visit(node)


def check_files(files):
    rc = RETURN_CODE['no_change']

    for fpath in files:
        with open(fpath) as f:
            source = f.read()

            try:
                tree = ast.parse(source, fpath)
            except SyntaxError:
                traceback.print_exc()
                return RETURN_CODE['syntax_error']

            visitor = IndentNodeVisitor()
            visitor.visit(tree)

            if visitor.lines:
                rc = RETURN_CODE['fixed_file']
                print('Fixing ' + fpath)
                fix_lines(
                    file_path=fpath,
                    source_lines=source.split('\n'),
                    line_data=visitor.lines,
                )

    return rc


def fix_lines(file_path, source_lines, line_data):
    line_data = sorted(line_data, key=itemgetter('line'))
    last_lineno = None
    same_line_adjustment = 0

    for i, data in enumerate(line_data):
        adjustment = 0
        lineno = data['line'] + i - 1

        if data['line'] == last_lineno:
            adjustment = same_line_adjustment

        start = 1 + source_lines[lineno].rfind(
            '(',
            0,
            data['column'] + adjustment,
        )

        nextline = source_lines[data['nextline'] + i - 1]
        indent = re.search('[ \t]*', nextline).group()
        new_line = indent + source_lines[lineno][start:]

        source_lines[lineno] = source_lines[lineno][:start]
        source_lines.insert(lineno + 1, new_line)

        with io.open(file_path, 'w') as f:
            f.write(u'\n'.join(source_lines))

        last_lineno = data['line']
        same_line_adjustment = len(indent) - start


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """
            Checks that parameters and arguments to functions, classes,
            and function calls are either all on the same line as the
            corresponding function or class or that none are.

            If it finds any violations, the offending parameters or arguments
            will automatically be moved to a new line.

            Return codes are:

                0: no file change
                1: file fixed
                2: Python syntax error
            """
        )
    )
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    return check_files(args.filenames)


if __name__ == '__main__':
    exit(main())
