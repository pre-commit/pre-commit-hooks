from typing import Optional
from typing import Sequence

from pre_commit_hooks.util import cmd_output


def main(argv: Optional[Sequence[str]] = None) -> int:
    # `argv` is ignored, pre-commit will send us a list of files that we
    # don't care about
    added_diff = cmd_output(
        'git', 'diff', '--staged', '--diff-filter=A', '--raw',
    )
    retv = 0
    for line in added_diff.splitlines():
        metadata, filename = line.split('\t', 1)
        new_mode = metadata.split(' ')[1]
        if new_mode == '160000':
            print(f'{filename}: new submodule introduced')
            retv = 1

    if retv:
        print()
        print('This commit introduces new submodules.')
        print('Did you unintentionally `git add .`?')
        print('To fix: git rm {thesubmodule}  # no trailing slash')
        print('Also check .gitmodules')

    return retv


if __name__ == '__main__':
    exit(main())
