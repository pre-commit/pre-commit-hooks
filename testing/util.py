from __future__ import annotations

import os.path
import subprocess


TESTING_DIR = os.path.abspath(os.path.dirname(__file__))


def get_resource_path(path):
    return os.path.join(TESTING_DIR, 'resources', path)


def git_commit(*args, **kwargs):
    cmd = ('git', 'commit', '--no-gpg-sign', '--no-verify', '--no-edit', *args)
    subprocess.check_call(cmd, **kwargs)


def get_default_branch():
    ret = subprocess.getoutput('git config init.defaultBranch').strip()
    return ret or 'master'
