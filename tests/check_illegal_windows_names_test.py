from __future__ import annotations

import os.path
import re

import pytest

from pre_commit_hooks.check_yaml import yaml


@pytest.fixture(scope='module')
def hook_re():
    here = os.path.dirname(__file__)
    with open(os.path.join(here, '..', '.pre-commit-hooks.yaml')) as f:
        hook_defs = yaml.load(f)
    hook, = (
        hook
        for hook in hook_defs
        if hook['id'] == 'check-illegal-windows-names'
    )
    yield re.compile(hook['files'])


@pytest.mark.parametrize(
    's',
    (
        pytest.param('aux.txt', id='with ext'),
        pytest.param('aux', id='without ext'),
        pytest.param('AuX.tXt', id='capitals'),
        pytest.param('com7.dat', id='com with digit'),
        pytest.param(':', id='bare colon'),
        pytest.param('file:Zone.Identifier', id='mid colon'),
    ),
)
def test_check_illegal_windows_names_matches(hook_re, s):
    assert hook_re.search(s)


@pytest.mark.parametrize(
    's',
    (
        pytest.param('README.md', id='standard file'),
        pytest.param('foo.aux', id='as ext'),
        pytest.param('com.dat', id='com without digit'),
    ),
)
def test_check_illegal_windows_names_does_not_match(hook_re, s):
    assert hook_re.search(s) is None
