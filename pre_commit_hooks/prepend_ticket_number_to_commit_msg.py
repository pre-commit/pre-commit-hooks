#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import io
import re
import subprocess
import sys

import six


def update_commit_message(filename, regex):
    with io.open(filename, 'r+') as fd:
        contents = fd.readlines()
        commit_msg = contents[0]
        # Check if we can grab ticket info from branch name.
        branch = get_branch_name()
        if all([
            not re.search(regex, commit_msg),
            re.search(regex, branch),
        ]):
            ticket = branch.split(six.text_type('_'))[0]
            new_commit_msg = '{} {}'.format(ticket, commit_msg)
            fd.seek(0)
            fd.write(
                six.text_type(
                    new_commit_msg,
                ),
            )
            fd.truncate()


def get_branch_name():
    # Only git support for right now.
    return subprocess.check_output(
        [
            'git',
            'rev-parse',
            '--abbrev-ref',
            'HEAD',
        ],
    ).decode('UTF-8')


def main(argv=None):
    """This hook saves developers time by prepending ticket numbers to commit-msgs.
    For this to work the following two conditions must be met:
        - The ticket format regex specified must match.
        - The branch name format must be <ticket number>_<rest of the branch name>
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+')
    parser.add_argument('--regex')
    args = parser.parse_args(argv)
    regex = args.regex or '[A-Z]+-\d+'  # noqa
    update_commit_message(args.filenames[0], regex)


if __name__ == '__main__':
    sys.exit(main())
