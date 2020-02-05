import pytest

from pre_commit_hooks.check_executables_have_shebangs import main


@pytest.mark.parametrize(
    'content', (
        b'#!/bin/bash\nhello world\n',
        b'#!/usr/bin/env python3.6',
        b'#!python',
        '#!☃'.encode(),
    ),
)
def test_has_shebang(content, tmpdir):
    path = tmpdir.join('path')
    path.write(content, 'wb')
    assert main((path.strpath,)) == 0


@pytest.mark.parametrize(
    'content', (
        b'',
        b' #!python\n',
        b'\n#!python\n',
        b'python\n',
        '☃'.encode(),

    ),
)
def test_bad_shebang(content, tmpdir, capsys):
    path = tmpdir.join('path')
    path.write(content, 'wb')
    assert main((path.strpath,)) == 1
    _, stderr = capsys.readouterr()
    assert stderr.startswith(f'{path}: marked executable but')
