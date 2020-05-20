import ast

import pytest

from pre_commit_hooks.check_builtin_literals import Call
from pre_commit_hooks.check_builtin_literals import main
from pre_commit_hooks.check_builtin_literals import Visitor

BUILTIN_CONSTRUCTORS = '''\
import builtins

c1 = complex()
d1 = dict()
f1 = float()
i1 = int()
l1 = list()
s1 = str()
t1 = tuple()

c2 = builtins.complex()
d2 = builtins.dict()
f2 = builtins.float()
i2 = builtins.int()
l2 = builtins.list()
s2 = builtins.str()
t2 = builtins.tuple()
'''
BUILTIN_LITERALS = '''\
c1 = 0j
d1 = {}
f1 = 0.0
i1 = 0
l1 = []
s1 = ''
t1 = ()
'''


@pytest.fixture
def visitor():
    return Visitor()


@pytest.mark.parametrize(
    ('expression', 'calls'),
    [
        # see #285
        ('x[0]()', []),
        # complex
        ('0j', []),
        ('complex()', [Call('complex', 1, 0)]),
        ('complex(0, 0)', []),
        ("complex('0+0j')", []),
        ('builtins.complex()', []),
        # float
        ('0.0', []),
        ('float()', [Call('float', 1, 0)]),
        ("float('0.0')", []),
        ('builtins.float()', []),
        # int
        ('0', []),
        ('int()', [Call('int', 1, 0)]),
        ("int('0')", []),
        ('builtins.int()', []),
        # list
        ('[]', []),
        ('list()', [Call('list', 1, 0)]),
        ("list('abc')", []),
        ("list([c for c in 'abc'])", []),
        ("list(c for c in 'abc')", []),
        ('builtins.list()', []),
        # str
        ("''", []),
        ('str()', [Call('str', 1, 0)]),
        ("str('0')", []),
        ('builtins.str()', []),
        # tuple
        ('()', []),
        ('tuple()', [Call('tuple', 1, 0)]),
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
        ('{}', []),
        ('dict()', [Call('dict', 1, 0)]),
        ('dict(a=1, b=2, c=3)', []),
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
        ('dict()', [Call('dict', 1, 0)]),
        ('dict(a=1, b=2, c=3)', [Call('dict', 1, 0)]),
        ("dict(**{'a': 1, 'b': 2, 'c': 3})", [Call('dict', 1, 0)]),
        ('builtins.dict()', []),
    ],
)
def test_dict_no_allow_kwargs_exprs(expression, calls):
    visitor = Visitor(allow_dict_kwargs=False)
    visitor.visit(ast.parse(expression))
    assert visitor.builtin_type_calls == calls


def test_ignore_constructors():
    visitor = Visitor(
        ignore=('complex', 'dict', 'float', 'int', 'list', 'str', 'tuple'),
    )
    visitor.visit(ast.parse(BUILTIN_CONSTRUCTORS))
    assert visitor.builtin_type_calls == []


def test_failing_file(tmpdir):
    f = tmpdir.join('f.py')
    f.write(BUILTIN_CONSTRUCTORS)
    rc = main([str(f)])
    assert rc == 1


def test_passing_file(tmpdir):
    f = tmpdir.join('f.py')
    f.write(BUILTIN_LITERALS)
    rc = main([str(f)])
    assert rc == 0


def test_failing_file_ignore_all(tmpdir):
    f = tmpdir.join('f.py')
    f.write(BUILTIN_CONSTRUCTORS)
    rc = main(['--ignore=complex,dict,float,int,list,str,tuple', str(f)])
    assert rc == 0
