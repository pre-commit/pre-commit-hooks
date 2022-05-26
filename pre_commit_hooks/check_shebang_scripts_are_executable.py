"""Check that text files with a shebang are executable."""
from __future__ import annotations

import argparse
import os
import shlex
import sys
from typing import Sequence

from pre_commit_hooks.check_executables_have_shebangs import EXECUTABLE_VALUES
from pre_commit_hooks.check_executables_have_shebangs import git_ls_files
from pre_commit_hooks.check_executables_have_shebangs import has_shebang
from pre_commit_hooks.util import cmd_output


def check_shebangs(paths: list[str]) -> int:
    fs_tracks_executable_bit = cmd_output(
        'git', 'config', 'core.fileMode', retcode=None,
    ).strip()
    return (
        _check_git_filemode(paths)
        if fs_tracks_executable_bit == 'false'
        else _check_fs_filemode(paths)
    )


def _check_fs_filemode(
    paths: list[str],
) -> int:  # pragma: win32 no cover
    retv = 0
    for path in paths:
        if not os.access(path, os.X_OK) and has_shebang(path):
            _message(path)
            retv = 1

    return retv


def _check_git_filemode(paths: Sequence[str]) -> int:
    seen: set[str] = set()
    for ls_file in git_ls_files(paths):
        is_executable = any(b in EXECUTABLE_VALUES for b in ls_file.mode[-3:])
        if not is_executable and has_shebang(ls_file.filename):
            _message(ls_file.filename)
            seen.add(ls_file.filename)

    return int(bool(seen))


def _message(path: str) -> None:
    print(
        f'{path}: has a shebang but is not marked executable!\n'
        f'  If it is supposed to be executable, try: '
        f'`chmod +x {shlex.quote(path)}`\n'
        f'  If on Windows, you may also need to: '
        f'`git add --chmod=+x {shlex.quote(path)}`\n'
        f'  If it not supposed to be executable, double-check its shebang '
        f'is wanted.\n',
        file=sys.stderr,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    return check_shebangs(args.filenames)


if __name__ == '__main__':
    raise SystemExit(main())
