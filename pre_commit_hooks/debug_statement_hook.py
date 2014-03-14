
import argparse
import ast
import collections
import sys


DEBUG_STATEMENTS = set(['pdb', 'ipdb', 'pudb'])


DebugStatement = collections.namedtuple(
    'DebugStatement', ['name', 'line', 'col'],
)


class ImportStatementParser(ast.NodeVisitor):
    def __init__(self):
        self.debug_import_statements = []

    def visit_Import(self, node):
        for node_name in node.names:
            if node_name.name in DEBUG_STATEMENTS:
                self.debug_import_statements.append(
                    DebugStatement(node_name.name, node.lineno, node.col_offset),
                )

    def visit_ImportFrom(self, node):
        if node.module in DEBUG_STATEMENTS:
            self.debug_import_statements.append(
                DebugStatement(node.module, node.lineno, node.col_offset)
            )


def check_file_for_debug_statements(filename):
    ast_obj = ast.parse(open(filename).read())
    visitor = ImportStatementParser()
    visitor.visit(ast_obj)
    if visitor.debug_import_statements:
        for debug_statement in visitor.debug_import_statements:
            print '{0}:{2}:{3} - {1} imported'.format(filename, *debug_statement)
        return 1
    else:
        return 0


def debug_statement_hook(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    args = parser.parse_args()

    retv = 0
    for filename in args.filenames:
        retv |= check_file_for_debug_statements(filename)

    return retv


def entry():
    return debug_statement_hook(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(entry())