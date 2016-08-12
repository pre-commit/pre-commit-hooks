from __future__ import absolute_import
from __future__ import unicode_literals

import os.path


TESTING_DIR = os.path.abspath(os.path.dirname(__file__))


def get_resource_path(path):
    return os.path.join(TESTING_DIR, 'resources', path)
