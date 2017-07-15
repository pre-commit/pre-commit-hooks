# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from pre_commit_hooks.check_executables_have_shebangs import main


@pytest.mark.parametrize(
    'content', (
        b'#!/bin/bash\nhello world\n',
        b'#!/usr/bin/env python3.6',
        b'#!python',
        '#!☃'.encode('UTF-8'),
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
        '☃'.encode('UTF-8'),

    ),
)
def test_bad_shebang(content, tmpdir, capsys):
    path = tmpdir.join('path')
    path.write(content, 'wb')
    assert main((path.strpath,)) == 1
    _, stderr = capsys.readouterr()
    assert stderr.startswith('{}: marked executable but'.format(path.strpath))
