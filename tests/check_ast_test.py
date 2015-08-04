from __future__ import absolute_import
from __future__ import unicode_literals

from pre_commit_hooks.check_ast import check_ast
from testing.util import get_resource_path


def test_failing_file():
    ret = check_ast([get_resource_path('cannot_parse_ast.notpy')])
    assert ret == 1


def test_passing_file():
    ret = check_ast([__file__])
    assert ret == 0
