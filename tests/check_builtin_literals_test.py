import ast

import pytest

from pre_commit_hooks.check_builtin_literals import BuiltinTypeCall
from pre_commit_hooks.check_builtin_literals import BuiltinTypeVisitor
from pre_commit_hooks.check_builtin_literals import main
from testing.util import get_resource_path


@pytest.fixture
def visitor():
    return BuiltinTypeVisitor()


@pytest.mark.parametrize(
    ('expression', 'calls'),
    [
        # see #285
        ('x[0]()', []),
        # complex
        ("0j", []),
        ("complex()", [BuiltinTypeCall('complex', 1, 0)]),
        ("complex(0, 0)", []),
        ("complex('0+0j')", []),
        ('builtins.complex()', []),
        # float
        ("0.0", []),
        ("float()", [BuiltinTypeCall('float', 1, 0)]),
        ("float('0.0')", []),
        ('builtins.float()', []),
        # int
        ("0", []),
        ("int()", [BuiltinTypeCall('int', 1, 0)]),
        ("int('0')", []),
        ('builtins.int()', []),
        # list
        ("[]", []),
        ("list()", [BuiltinTypeCall('list', 1, 0)]),
        ("list('abc')", []),
        ("list([c for c in 'abc'])", []),
        ("list(c for c in 'abc')", []),
        ('builtins.list()', []),
        # str
        ("''", []),
        ("str()", [BuiltinTypeCall('str', 1, 0)]),
        ("str('0')", []),
        ('builtins.str()', []),
        # tuple
        ("()", []),
        ("tuple()", [BuiltinTypeCall('tuple', 1, 0)]),
        ("tuple('abc')", []),
        ("tuple([c for c in 'abc'])", []),
        ("tuple(c for c in 'abc')", []),
        ('builtins.tuple()', []),
    ],
)
def test_non_dict_exprs(visitor, expression, calls):
    visitor.visit(ast.parse(expression))
    assert visitor.builtin_type_calls == calls


@pytest.mark.parametrize(
    ('expression', 'calls'),
    [
        ("{}", []),
        ("dict()", [BuiltinTypeCall('dict', 1, 0)]),
        ("dict(a=1, b=2, c=3)", []),
        ("dict(**{'a': 1, 'b': 2, 'c': 3})", []),
        ("dict([(k, v) for k, v in [('a', 1), ('b', 2), ('c', 3)]])", []),
        ("dict((k, v) for k, v in [('a', 1), ('b', 2), ('c', 3)])", []),
        ('builtins.dict()', []),
    ],
)
def test_dict_allow_kwargs_exprs(visitor, expression, calls):
    visitor.visit(ast.parse(expression))
    assert visitor.builtin_type_calls == calls


@pytest.mark.parametrize(
    ('expression', 'calls'),
    [
        ("dict()", [BuiltinTypeCall('dict', 1, 0)]),
        ("dict(a=1, b=2, c=3)", [BuiltinTypeCall('dict', 1, 0)]),
        ("dict(**{'a': 1, 'b': 2, 'c': 3})", [BuiltinTypeCall('dict', 1, 0)]),
        ('builtins.dict()', []),
    ],
)
def test_dict_no_allow_kwargs_exprs(expression, calls):
    visitor = BuiltinTypeVisitor(allow_dict_kwargs=False)
    visitor.visit(ast.parse(expression))
    assert visitor.builtin_type_calls == calls


def test_ignore_constructors():
    visitor = BuiltinTypeVisitor(ignore=('complex', 'dict', 'float', 'int', 'list', 'str', 'tuple'))
    visitor.visit(ast.parse(open(get_resource_path('builtin_constructors.py'), 'rb').read(), 'builtin_constructors.py'))
    assert visitor.builtin_type_calls == []


def test_failing_file():
    rc = main([get_resource_path('builtin_constructors.py')])
    assert rc == 1


def test_passing_file():
    rc = main([get_resource_path('builtin_literals.py')])
    assert rc == 0


def test_failing_file_ignore_all():
    rc = main([
        '--ignore=complex,dict,float,int,list,str,tuple',
        get_resource_path('builtin_constructors.py'),
    ])
    assert rc == 0
