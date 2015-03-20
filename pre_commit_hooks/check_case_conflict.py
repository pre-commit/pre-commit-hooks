from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse

from pre_commit_hooks.util import added_files
from pre_commit_hooks.util import cmd_output


def lower_set(iterable):
    return set(x.lower() for x in iterable)


def find_conflicting_filenames(filenames):
    repo_files = set(cmd_output('git', 'ls-files').splitlines())
    relevant_files = set(filenames) | added_files()
    repo_files -= relevant_files
    retv = 0

    # new file conflicts with existing file
    conflicts = lower_set(repo_files) & lower_set(relevant_files)

    # new file conflicts with other new file
    lowercase_relevant_files = lower_set(relevant_files)
    for filename in set(relevant_files):
        if filename.lower() in lowercase_relevant_files:
            lowercase_relevant_files.remove(filename.lower())
        else:
            conflicts.add(filename.lower())

    if conflicts:
        conflicting_files = [
            x for x in repo_files | relevant_files
            if x.lower() in conflicts
        ]
        for filename in sorted(conflicting_files):
            print('Case-insensitivity conflict found: {0}'.format(filename))
        retv = 1

    return retv


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.'
    )

    args = parser.parse_args(argv)

    return find_conflicting_filenames(args.filenames)


if __name__ == '__main__':
    exit(main())
