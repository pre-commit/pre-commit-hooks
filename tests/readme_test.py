from __future__ import absolute_import
from __future__ import unicode_literals

import io

from pre_commit_hooks.check_yaml import yaml


def test_readme_contains_all_hooks():
    with io.open('README.md', encoding='UTF-8') as f:
        readme_contents = f.read()
    with io.open('.pre-commit-hooks.yaml', encoding='UTF-8') as f:
        hooks = yaml.load(f)
    for hook in hooks:
        assert '`{}`'.format(hook['id']) in readme_contents
