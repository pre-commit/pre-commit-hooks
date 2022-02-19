"""Check that executable text files have a shebang."""
from __future__ import annotations

import argparse
import shlex
import sys
from typing import Generator
from typing import NamedTuple
from typing import Sequence

from pre_commit_hooks.util import cmd_output
from pre_commit_hooks.util import zsplit

EXECUTABLE_VALUES = frozenset(('1', '3', '5', '7'))


def check_executables(paths: list[str]) -> int:
    fs_tracks_executable_bit = cmd_output(
        'git', 'config', 'core.fileMode', retcode=None,
    ).strip()
    if fs_tracks_executable_bit == 'false':  # pragma: win32 cover
        return _check_git_filemode(paths)
    else:  # pragma: win32 no cover
        retv = 0
        for path in paths:
            if not has_shebang(path):
                _message(path)
                retv = 1

        return retv


class GitLsFile(NamedTuple):
    mode: str
    filename: str


def git_ls_files(paths: Sequence[str]) -> Generator[GitLsFile, None, None]:
    outs = cmd_output('git', 'ls-files', '-z', '--stage', '--', *paths)
    for out in zsplit(outs):
        metadata, filename = out.split('\t')
        mode, _, _ = metadata.split()
        yield GitLsFile(mode, filename)


def _check_git_filemode(paths: Sequence[str]) -> int:
    seen: set[str] = set()
    for ls_file in git_ls_files(paths):
        is_executable = any(b in EXECUTABLE_VALUES for b in ls_file.mode[-3:])
        if is_executable and not has_shebang(ls_file.filename):
            _message(ls_file.filename)
            seen.add(ls_file.filename)

    return int(bool(seen))


def has_shebang(path: str) -> int:
    with open(path, 'rb') as f:
        first_bytes = f.read(2)

    return first_bytes == b'#!'


def _message(path: str) -> None:
    print(
        f'{path}: marked executable but has no (or invalid) shebang!\n'
        f"  If it isn't supposed to be executable, try: "
        f'`chmod -x {shlex.quote(path)}`\n'
        f'  If on Windows, you may also need to: '
        f'`git add --chmod=-x {shlex.quote(path)}`\n'
        f'  If it is supposed to be executable, double-check its shebang.',
        file=sys.stderr,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    return check_executables(args.filenames)


if __name__ == '__main__':
    raise SystemExit(main())
