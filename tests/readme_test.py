from __future__ import absolute_import
from __future__ import unicode_literals

import yaml


def test_readme_contains_all_hooks():
    readme_contents = open('README.md').read()
    hooks = yaml.load(open('hooks.yaml').read())
    for hook in hooks:
        assert '`{}`'.format(hook['id']) in readme_contents
