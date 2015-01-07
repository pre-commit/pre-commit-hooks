from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from plumbum import local


def added_files():
    return set(local['git'](
        'diff', '--staged', '--name-only', '--diff-filter', 'A',
    ).splitlines())
