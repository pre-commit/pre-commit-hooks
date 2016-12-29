from __future__ import absolute_import
from __future__ import unicode_literals

import os.path


TESTING_DIR = os.path.abspath(os.path.dirname(__file__))


def get_resource_path(path):
    return os.path.join(TESTING_DIR, 'resources', path)


def write_file(filename, contents):
    """Hax because coveragepy chokes on nested context managers."""
    with open(filename, 'w', newline='') as file_obj:
        file_obj.write(contents)
