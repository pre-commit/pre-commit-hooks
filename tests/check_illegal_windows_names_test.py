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
        pytest.param('path/COM¹.json', id='com with superscript'),
        pytest.param('dir/LPT³.toml', id='lpt with superscript'),
        pytest.param('with < less than', id='with less than'),
        pytest.param('Fast or Slow?.md', id='with question mark'),
        pytest.param('with "double" quotes', id='with double quotes'),
        pytest.param('with_null\x00byte', id='with null byte'),
        pytest.param('ends_with.', id='ends with period'),
        pytest.param('ends_with ', id='ends with space'),
        pytest.param('ends_with\t', id='ends with tab'),
        pytest.param('dir/ends./with.txt', id='directory ends with period'),
        pytest.param('dir/ends /with.txt', id='directory ends with space'),
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
        pytest.param('.python-version', id='starts with period'),
        pytest.param(' pseudo nan', id='with spaces'),
        pytest.param('!@#$%^&;=≤\'~`¡¿€🤗', id='with allowed characters'),
        pytest.param('path.to/file.py', id='standard path'),
    ),
)
def test_check_illegal_windows_names_does_not_match(hook_re, s):
    assert hook_re.search(s) is None
