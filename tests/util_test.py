import pytest

from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output
from pre_commit_hooks.util import zsplit


def test_raises_on_error():
    with pytest.raises(CalledProcessError):
        cmd_output('sh', '-c', 'exit 1')


def test_output():
    ret = cmd_output('sh', '-c', 'echo hi')
    assert ret == 'hi\n'


@pytest.mark.parametrize('out', ('\0f1\0f2\0', '\0f1\0f2', 'f1\0f2\0'))
def test_check_zsplits_str_correctly(out):
    assert zsplit(out) == ['f1', 'f2']


@pytest.mark.parametrize('out', ('\0\0', '\0', ''))
def test_check_zsplit_returns_empty(out):
    assert zsplit(out) == []
