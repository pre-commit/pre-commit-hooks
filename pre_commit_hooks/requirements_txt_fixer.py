from __future__ import annotations

import argparse
import re
from collections.abc import Sequence
from typing import IO


PASS = 0
FAIL = 1


class Requirement:
    UNTIL_COMPARISON = re.compile(b'={2,3}|!=|~=|>=?|<=?')
    UNTIL_SEP = re.compile(rb'[^;\s]+')
    VERSION_SPECIFIED = re.compile(b'.+(={2,3}|!=|~=|>=?|<=?).+')

    def __init__(self) -> None:
        self.value: bytes | None = None
        self.comments: list[bytes] = []

    @property
    def name(self) -> bytes:
        assert self.value is not None, self.value
        name = self.value.lower()
        for egg in (b'#egg=', b'&egg='):
            if egg in self.value:
                return name.partition(egg)[-1]

        m = self.UNTIL_SEP.match(name)
        assert m is not None

        name = m.group()
        m = self.UNTIL_COMPARISON.search(name)
        if not m:
            return name

        return name[:m.start()]

    def __lt__(self, requirement: Requirement) -> bool:
        # \n means top of file comment, so always return True,
        # otherwise just do a string comparison with value.
        assert self.value is not None, self.value
        if self.value == b'\n':
            return True
        elif requirement.value == b'\n':
            return False
        else:
            # if 2 requirements have the same name, the one with comments
            # needs to go first (so that when removing duplicates, the one
            # with comments is kept)
            if self.name == requirement.name:
                return bool(self.comments) > bool(requirement.comments)
            return self.name < requirement.name

    def is_complete(self) -> bool:
        return (
            self.value is not None and
            not self.value.rstrip(b'\r\n').endswith(b'\\')
        )

    def contains_version_specifier(self) -> bool:
        return (
            self.value is not None and
            bool(self.VERSION_SPECIFIED.match(self.value))
        )

    def append_value(self, value: bytes) -> None:
        if self.value is not None:
            self.value += value
        else:
            self.value = value


def fix_requirements(f: IO[bytes], fail_without_version: bool) -> int:
    requirements: list[Requirement] = []
    before = list(f)
    after: list[bytes] = []

    before_string = b''.join(before)

    # adds new line in case one is missing
    # AND a change to the requirements file is needed regardless:
    if before and not before[-1].endswith(b'\n'):
        before[-1] += b'\n'

    # If the file is empty (i.e. only whitespace/newlines) exit early
    if before_string.strip() == b'':
        return PASS

    for line in before:
        # If the most recent requirement object has a value, then it's
        # time to start building the next requirement object.

        if not len(requirements) or requirements[-1].is_complete():
            requirements.append(Requirement())

        requirement = requirements[-1]

        # If we see a newline before any requirements, then this is a
        # top of file comment.
        if len(requirements) == 1 and line.strip() == b'':
            if (
                    len(requirement.comments) and
                    requirement.comments[0].startswith(b'#')
            ):
                requirement.value = b'\n'
            else:
                requirement.comments.append(line)
        elif line.lstrip().startswith(b'#') or line.strip() == b'':
            requirement.comments.append(line)
        else:
            requirement.append_value(line)

    # if a file ends in a comment, preserve it at the end
    if requirements[-1].value is None:
        rest = requirements.pop().comments
    else:
        rest = []

    # find and remove pkg-resources==0.0.0
    # which is automatically added by broken pip package under Debian
    requirements = [
        req for req in requirements
        if req.value not in [
            b'pkg-resources==0.0.0\n',
            b'pkg_resources==0.0.0\n',
        ]
    ]

    # check for requirements without a version specified
    if fail_without_version:
        missing_requirement_found = False
        for req in requirements:
            if not req.contains_version_specifier():
                print(f'Missing version for requirement {req.name.decode()}')
                missing_requirement_found = True

        if missing_requirement_found:
            return FAIL

    # sort the requirements and remove duplicates
    prev = None
    for requirement in sorted(requirements):
        after.extend(requirement.comments)
        assert requirement.value, requirement.value
        if prev is None or requirement.value != prev.value:
            after.append(requirement.value)
            prev = requirement
    after.extend(rest)

    after_string = b''.join(after)

    if before_string == after_string:
        return PASS
    else:
        print('Sorting requirements')
        f.seek(0)
        f.write(after_string)
        f.truncate()
        return FAIL


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    parser.add_argument(
        '--fail-without-version', action='store_true',
        help='Fail if a requirement is missing a version',
    )
    args = parser.parse_args(argv)

    retv = PASS

    for arg in args.filenames:
        with open(arg, 'rb+') as file_obj:
            ret_for_file = fix_requirements(
                file_obj, args.fail_without_version,
            )

            if ret_for_file:
                print(f'Error in file {arg}')

            retv |= ret_for_file

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
