from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import io
import sys

import yapf


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    return yapf.main(argv)


if __name__ == '__main__':
    exit(main())
