from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from pre_commit_hooks.check_yaml import check_yaml
from testing.util import get_resource_path


@pytest.mark.parametrize(
    ('filename', 'expected_retval'), (
        ('bad_yaml.notyaml', 1),
        ('ok_yaml.yaml', 0),
    ),
)
def test_check_yaml(filename, expected_retval):
    ret = check_yaml([get_resource_path(filename)])
    assert ret == expected_retval


def test_check_yaml_allow_multiple_documents(tmpdir):
    f = tmpdir.join('test.yaml')
    f.write('---\nfoo\n---\nbar\n')

    # should fail without the setting
    assert check_yaml((f.strpath,))

    # should pass when we allow multiple documents
    assert not check_yaml(('--allow-multiple-documents', f.strpath))


def test_fails_even_with_allow_multiple_documents(tmpdir):
    f = tmpdir.join('test.yaml')
    f.write('[')
    assert check_yaml(('--allow-multiple-documents', f.strpath))


def test_check_yaml_unsafe(tmpdir):
    f = tmpdir.join('test.yaml')
    f.write(
        'some_foo: !vault |\n'
        '    $ANSIBLE_VAULT;1.1;AES256\n'
        '    deadbeefdeadbeefdeadbeef\n',
    )
    # should fail "safe" check
    assert check_yaml((f.strpath,))
    # should pass when we allow unsafe documents
    assert not check_yaml(('--unsafe', f.strpath))


def test_check_yaml_unsafe_still_fails_on_syntax_errors(tmpdir):
    f = tmpdir.join('test.yaml')
    f.write('[')
    assert check_yaml(('--unsafe', f.strpath))
