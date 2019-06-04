import subprocess
import sys
import uuid

import pytest

from pre_commit_hooks.loaderon_hooks.general_hooks.check_branch_name import main


@pytest.fixture(autouse=True)
def clean_sys_argv():
    sys.argv = []
    yield


def test_docstring_ok():
    new_branch_name = str(uuid.uuid4())
    subprocess.check_output(['git', 'checkout', '-b', new_branch_name])
    sys.argv.append('--regex')
    sys.argv.append(r'\b(?!master)\b\S+')

    result = main(sys.argv)

    subprocess.check_output(['git', 'checkout', 'master'])
    subprocess.check_output(['git', 'branch', '-d', new_branch_name])

    assert result == 0


def test_branch_name_error():
    subprocess.check_output(['git', 'checkout', 'master'])
    sys.argv.append('--regex')
    sys.argv.append(r'\b(?!master)\b\S+')

    result = main(sys.argv)

    assert result == 2
