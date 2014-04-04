
import subprocess

from pre_commit.clientlib.validate_manifest import load_manifest


def test_all_hooks_allow_no_files():
    manifest = load_manifest('hooks.yaml')

    for hook in manifest:
        if hook['id'] != 'pyflakes':
            subprocess.check_call([hook['entry']])
