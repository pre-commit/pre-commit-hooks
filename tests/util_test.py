import pytest

from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output


def test_raises_on_error():
    with pytest.raises(CalledProcessError):
        cmd_output('sh', '-c', 'exit 1')


def test_output():
    ret = cmd_output('sh', '-c', 'echo hi')
    assert ret == 'hi\n'
