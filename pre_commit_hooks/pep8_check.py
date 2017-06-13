from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import sys
import xml.sax
from pre_commit_hooks.util import cmd_output


def check_pep8(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='XML filenames to check.')
    args = parser.parse_args(argv)
    print (args)

    retval = 0
    lines = cmd_output("git diff --cached -- '*.py' | "
                       "`which pep8` --max-line-length=119 --show-source --diff --ignore=E402,E731").splitlines()
    if len(lines) > 0:
        print (lines)
        retval = 1
    return retval
