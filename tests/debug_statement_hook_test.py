
import ast
import pytest

from pre_commit_hooks.debug_statement_hook import ImportStatementParser, \
    DebugStatement


@pytest.fixture
def ast_with_no_debug_imports():
    return ast.parse("""
import foo
import bar
import baz
from foo import bar
""")


@pytest.fixture
def ast_with_debug_import_form_1():
    return ast.parse("""

import ipdb; ipdb.set_trace()

""")


@pytest.fixture
def ast_with_debug_import_form_2():
    return ast.parse("""

from pudb import set_trace; set_trace()

""")


def test_returns_no_debug_statements(ast_with_no_debug_imports):
    visitor = ImportStatementParser()
    visitor.visit(ast_with_no_debug_imports)
    assert visitor.debug_import_statements == []


def test_returns_one_form_1(ast_with_debug_import_form_1):
    visitor = ImportStatementParser()
    visitor.visit(ast_with_debug_import_form_1)
    assert visitor.debug_import_statements == [
        DebugStatement('ipdb', 3, 0)
    ]


def test_returns_one_form_2(ast_with_debug_import_form_2):
    visitor = ImportStatementParser()
    visitor.visit(ast_with_debug_import_form_2)
    assert visitor.debug_import_statements == [
        DebugStatement('pudb', 3, 0)
    ]