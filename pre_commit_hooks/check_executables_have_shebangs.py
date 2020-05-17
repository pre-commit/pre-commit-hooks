"""Check that executable text files have a shebang."""
import argparse
import shlex
import sys
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set

from pre_commit_hooks.util import cmd_output

EXECUTABLE_VALUES = frozenset(('1', '3', '5', '7'))


def check_executables(paths: List[str]) -> int:
    if sys.platform == 'win32':  # pragma: win32 cover
        return _check_git_filemode(paths)
    else:  # pragma: win32 no cover
        retv = 0
        for path in paths:
            if not _check_has_shebang(path):
                _message(path)
                retv = 1

        return retv


def _check_git_filemode(paths: Sequence[str]) -> int:
    outs = cmd_output('git', 'ls-files', '--stage', '--', *paths)
    seen: Set[str] = set()
    for out in outs.splitlines():
        metadata, path = out.split('\t')
        tagmode = metadata.split(' ', 1)[0]

        is_executable = any(b in EXECUTABLE_VALUES for b in tagmode[-3:])
        has_shebang = _check_has_shebang(path)
        if is_executable and not has_shebang:
            _message(path)
            seen.add(path)

    return int(bool(seen))


def _check_has_shebang(path: str) -> int:
    with open(path, 'rb') as f:
        first_bytes = f.read(2)

    return first_bytes == b'#!'


def _message(path: str) -> None:
    print(
        f'{path}: marked executable but has no (or invalid) shebang!\n'
        f"  If it isn't supposed to be executable, try: "
        f'`chmod -x {shlex.quote(path)}`\n'
        f'  If it is supposed to be executable, double-check its shebang.',
        file=sys.stderr,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    return check_executables(args.filenames)


if __name__ == '__main__':
    exit(main())
