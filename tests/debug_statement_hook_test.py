# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import ast

from pre_commit_hooks.debug_statement_hook import debug_statement_hook
from pre_commit_hooks.debug_statement_hook import DebugStatement
from pre_commit_hooks.debug_statement_hook import ImportStatementParser
from testing.util import get_resource_path


def test_no_debug_imports():
    visitor = ImportStatementParser()
    visitor.visit(ast.parse('import os\nfrom foo import bar\n'))
    assert visitor.debug_import_statements == []


def test_finds_debug_import_attribute_access():
    visitor = ImportStatementParser()
    visitor.visit(ast.parse('import ipdb; ipdb.set_trace()'))
    assert visitor.debug_import_statements == [DebugStatement('ipdb', 1, 0)]


def test_finds_debug_import_from_import():
    visitor = ImportStatementParser()
    visitor.visit(ast.parse('from pudb import set_trace; set_trace()'))
    assert visitor.debug_import_statements == [DebugStatement('pudb', 1, 0)]


def test_returns_one_for_failing_file(tmpdir):
    f_py = tmpdir.join('f.py')
    f_py.write('def f():\n    import pdb; pdb.set_trace()')
    ret = debug_statement_hook([f_py.strpath])
    assert ret == 1


def test_returns_zero_for_passing_file():
    ret = debug_statement_hook([__file__])
    assert ret == 0


def test_syntaxerror_file():
    ret = debug_statement_hook([get_resource_path('cannot_parse_ast.notpy')])
    assert ret == 1


def test_non_utf8_file(tmpdir):
    f_py = tmpdir.join('f.py')
    f_py.write_binary('# -*- coding: cp1252 -*-\nx = "€"\n'.encode('cp1252'))
    assert debug_statement_hook((f_py.strpath,)) == 0
