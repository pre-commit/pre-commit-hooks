import os
import sys

import pytest

from pre_commit_hooks import check_executables_have_shebangs
from pre_commit_hooks.check_executables_have_shebangs import main
from pre_commit_hooks.util import cmd_output

skip_win32 = pytest.mark.skipif(
    sys.platform == 'win32',
    reason="non-git checks aren't relevant on windows",
)


@skip_win32  # pragma: win32 no cover
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
    assert main((str(path),)) == 0


@skip_win32  # pragma: win32 no cover
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
    assert main((str(path),)) == 1
    _, stderr = capsys.readouterr()
    assert stderr.startswith(f'{path}: marked executable but')


def test_check_git_filemode_passing(tmpdir):
    with tmpdir.as_cwd():
        cmd_output('git', 'init', '.')

        f = tmpdir.join('f')
        f.write('#!/usr/bin/env bash')
        f_path = str(f)
        cmd_output('chmod', '+x', f_path)
        cmd_output('git', 'add', f_path)
        cmd_output('git', 'update-index', '--chmod=+x', f_path)

        g = tmpdir.join('g').ensure()
        g_path = str(g)
        cmd_output('git', 'add', g_path)

        # this is potentially a problem, but not something the script intends
        # to check for -- we're only making sure that things that are
        # executable have shebangs
        h = tmpdir.join('h')
        h.write('#!/usr/bin/env bash')
        h_path = str(h)
        cmd_output('git', 'add', h_path)

        files = (f_path, g_path, h_path)
        assert check_executables_have_shebangs._check_git_filemode(files) == 0


def test_check_git_filemode_failing(tmpdir):
    with tmpdir.as_cwd():
        cmd_output('git', 'init', '.')

        f = tmpdir.join('f').ensure()
        f_path = str(f)
        cmd_output('chmod', '+x', f_path)
        cmd_output('git', 'add', f_path)
        cmd_output('git', 'update-index', '--chmod=+x', f_path)

        files = (f_path,)
        assert check_executables_have_shebangs._check_git_filemode(files) == 1


@pytest.mark.parametrize(
    ('content', 'mode', 'expected'),
    (
        pytest.param('#!python', '+x', 0, id='shebang with executable'),
        pytest.param('#!python', '-x', 0, id='shebang without executable'),
        pytest.param('', '+x', 1, id='no shebang with executable'),
        pytest.param('', '-x', 0, id='no shebang without executable'),
    ),
)
def test_git_executable_shebang(temp_git_dir, content, mode, expected):
    with temp_git_dir.as_cwd():
        path = temp_git_dir.join('path')
        path.write(content)
        cmd_output('git', 'add', str(path))
        cmd_output('chmod', mode, str(path))
        cmd_output('git', 'update-index', f'--chmod={mode}', str(path))

        # simulate how identify chooses that something is executable
        filenames = [path for path in [str(path)] if os.access(path, os.X_OK)]

        assert main(filenames) == expected
