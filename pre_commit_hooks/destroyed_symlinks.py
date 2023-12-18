from __future__ import annotations

import argparse
import shlex
import subprocess
from typing import Sequence

from pre_commit_hooks.util import cmd_output
from pre_commit_hooks.util import zsplit

ORDINARY_CHANGED_ENTRIES_MARKER = '1'
PERMS_LINK = '120000'
PERMS_NONEXIST = '000000'


def find_destroyed_symlinks(files: Sequence[str]) -> list[str]:
    destroyed_links: list[str] = []
    if not files:
        return destroyed_links
    for line in zsplit(
        cmd_output('git', 'status', '--porcelain=v2', '-z', '--', *files),
    ):
        splitted = line.split(' ')
        if splitted and splitted[0] == ORDINARY_CHANGED_ENTRIES_MARKER:
            # https://git-scm.com/docs/git-status#_changed_tracked_entries
            (
                _, _, _,
                mode_HEAD,
                mode_index,
                _,
                hash_HEAD,
                hash_index,
                *path_splitted,
            ) = splitted
            path = ' '.join(path_splitted)
            if (
                    mode_HEAD == PERMS_LINK and
                    mode_index != PERMS_LINK and
                    mode_index != PERMS_NONEXIST
            ):
                if hash_HEAD == hash_index:
                    # if old and new hashes are equal, it's not needed to check
                    # anything more, we've found a destroyed symlink for sure
                    destroyed_links.append(path)
                else:
                    # if old and new hashes are *not* equal, it doesn't mean
                    # that everything is OK - new file may be altered
                    # by something like trailing-whitespace and/or
                    # mixed-line-ending hooks so we need to go deeper
                    SIZE_CMD = ('git', 'cat-file', '-s')
                    size_index = int(cmd_output(*SIZE_CMD, hash_index).strip())
                    size_HEAD = int(cmd_output(*SIZE_CMD, hash_HEAD).strip())

                    # in the worst case new file may have CRLF added
                    # so check content only if new file is bigger
                    # not more than 2 bytes compared to the old one
                    if size_index <= size_HEAD + 2:
                        head_content = subprocess.check_output(
                            ('git', 'cat-file', '-p', hash_HEAD),
                        ).rstrip()
                        index_content = subprocess.check_output(
                            ('git', 'cat-file', '-p', hash_index),
                        ).rstrip()
                        if head_content == index_content:
                            destroyed_links.append(path)
    return destroyed_links


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)
    destroyed_links = find_destroyed_symlinks(files=args.filenames)
    if destroyed_links:
        print('Destroyed symlinks:')
        for destroyed_link in destroyed_links:
            print(f'- {destroyed_link}')
        print('You should unstage affected files:')
        print(f'\tgit reset HEAD -- {shlex.join(destroyed_links)}')
        print(
            'And retry commit. As a long term solution '
            'you may try to explicitly tell git that your '
            'environment does not support symlinks:',
        )
        print('\tgit config core.symlinks false')
        return 1
    else:
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
