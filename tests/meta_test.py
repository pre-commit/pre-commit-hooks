from __future__ import absolute_import
from __future__ import unicode_literals

import io

import yaml


def _assert_parseable_in_old_pre_commit(hooks):
    for hook in hooks:
        assert {'id', 'name', 'entry', 'files', 'language'} <= set(hook)


def test_legacy_hooks():
    with io.open('hooks.yaml') as legacy_file:
        legacy = yaml.load(legacy_file.read())
    with io.open('.pre-commit-hooks.yaml') as hooks_file:
        hooks = yaml.load(hooks_file.read())

    # The same set of hooks should be defined in both files
    new_hook_ids = {hook['id'] for hook in hooks}
    legacy_hook_ids = {hook['id'] for hook in legacy}
    assert new_hook_ids == legacy_hook_ids

    # Both files should be parseable by pre-commit<0.15.0
    _assert_parseable_in_old_pre_commit(legacy)
    _assert_parseable_in_old_pre_commit(hooks)

    # The legacy file should force upgrading
    for hook in legacy:
        del hook['id']
        assert hook == {
            'language': 'system',
            'name': 'upgrade-your-pre-commit-version',
            'entry': 'upgrade-your-pre-commit-version',
            'files': '',
            'minimum_pre_commit_version': '0.15.0',
        }

    # Each hook should require a new version if it uses types
    for hook in hooks:
        if 'types' in hook:
            assert hook['minimum_pre_commit_version'] == '0.15.0'
