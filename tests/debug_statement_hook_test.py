import ast

from pre_commit_hooks.debug_statement_hook import Debug
from pre_commit_hooks.debug_statement_hook import DebugStatementParser
from pre_commit_hooks.debug_statement_hook import main
from testing.util import get_resource_path


def test_no_breakpoints():
    visitor = DebugStatementParser()
    visitor.visit(ast.parse('import os\nfrom foo import bar\n'))
    assert visitor.breakpoints == []


def test_finds_debug_import_attribute_access():
    visitor = DebugStatementParser()
    visitor.visit(ast.parse('import ipdb; ipdb.set_trace()'))
    assert visitor.breakpoints == [Debug(1, 0, 'ipdb', 'imported')]


def test_finds_debug_import_from_import():
    visitor = DebugStatementParser()
    visitor.visit(ast.parse('from pudb import set_trace; set_trace()'))
    assert visitor.breakpoints == [Debug(1, 0, 'pudb', 'imported')]


def test_finds_breakpoint():
    visitor = DebugStatementParser()
    visitor.visit(ast.parse('breakpoint()'))
    assert visitor.breakpoints == [Debug(1, 0, 'breakpoint', 'called')]


def test_returns_one_for_failing_file(tmpdir):
    f_py = tmpdir.join('f.py')
    f_py.write('def f():\n    import pdb; pdb.set_trace()')
    ret = main([str(f_py)])
    assert ret == 1


def test_returns_zero_for_passing_file():
    ret = main([__file__])
    assert ret == 0


def test_syntaxerror_file():
    ret = main([get_resource_path('cannot_parse_ast.notpy')])
    assert ret == 1


def test_non_utf8_file(tmpdir):
    f_py = tmpdir.join('f.py')
    f_py.write_binary('# -*- coding: cp1252 -*-\nx = "€"\n'.encode('cp1252'))
    assert main((str(f_py),)) == 0


def test_py37_breakpoint(tmpdir):
    f_py = tmpdir.join('f.py')
    f_py.write('def f():\n    breakpoint()\n')
    assert main((str(f_py),)) == 1
