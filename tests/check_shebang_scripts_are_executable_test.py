from __future__ import annotations

import os
import sys
from types import SimpleNamespace

import pytest

import pre_commit_hooks.check_shebang_scripts_are_executable as shebang_hook
from pre_commit_hooks.check_shebang_scripts_are_executable import \
    _check_git_filemode
from pre_commit_hooks.check_shebang_scripts_are_executable import main
from pre_commit_hooks.util import cmd_output


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

        files = [f_path, g_path]
        assert _check_git_filemode(files) == 0

        # this is the one we should trigger on
        h = tmpdir.join('h')
        h.write('#!/usr/bin/env bash')
        h_path = str(h)
        cmd_output('git', 'add', h_path)

        files = [h_path]
        assert _check_git_filemode(files) == 1


def test_check_git_filemode_passing_unusual_characters(tmpdir):
    with tmpdir.as_cwd():
        cmd_output('git', 'init', '.')

        f = tmpdir.join('mañana.txt')
        f.write('#!/usr/bin/env bash')
        f_path = str(f)
        cmd_output('chmod', '+x', f_path)
        cmd_output('git', 'add', f_path)
        cmd_output('git', 'update-index', '--chmod=+x', f_path)

        files = (f_path,)
        assert _check_git_filemode(files) == 0


def test_check_git_filemode_failing(tmpdir):
    with tmpdir.as_cwd():
        cmd_output('git', 'init', '.')

        f = tmpdir.join('f').ensure()
        f.write('#!/usr/bin/env bash')
        f_path = str(f)
        cmd_output('git', 'add', f_path)

        files = (f_path,)
        assert _check_git_filemode(files) == 1


@pytest.mark.parametrize(
    ('content', 'mode', 'expected'),
    (
        pytest.param('#!python', '+x', 0, id='shebang with executable'),
        pytest.param('#!python', '-x', 1, id='shebang without executable'),
        pytest.param('', '+x', 0, id='no shebang with executable'),
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


@pytest.mark.parametrize(
    ('content', 'executable', 'expected'),
    (
        ('#!/bin/sh\n', False, 1),
        ('#!/bin/sh\n', True, 0),
        ('echo hello\n', False, 0),
    ),
)
def test_without_git_repository(tmp_path, monkeypatch, content, executable, expected):
    script = tmp_path / 'example.sh'
    script.write_text(content)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        shebang_hook, 'os',
        SimpleNamespace(access=lambda path, mode: executable, X_OK=os.X_OK),
    )
    monkeypatch.setattr(
        shebang_hook, 'sys', SimpleNamespace(platform='linux', stderr=sys.stderr),
    )

    assert main([str(script)]) == expected


def test_without_git_repository_on_windows_raises(tmp_path, monkeypatch):
    script = tmp_path / 'example.sh'
    script.write_text('#!/bin/sh\n')
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        shebang_hook, 'sys', SimpleNamespace(platform='win32', stderr=sys.stderr),
    )

    with pytest.raises(shebang_hook.CalledProcessError):
        main([str(script)])


def test_git_failure_inside_repository_is_not_hidden(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cmd_output('git', 'init', '.')

    def broken_ls_files(paths):
        raise shebang_hook.CalledProcessError('simulated git error')

    monkeypatch.setattr(shebang_hook, 'git_ls_files', broken_ls_files)

    with pytest.raises(shebang_hook.CalledProcessError, match='simulated'):
        main([])
