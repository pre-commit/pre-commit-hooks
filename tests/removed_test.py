import pytest

from pre_commit_hooks.removed import main


def test_always_fails():
    with pytest.raises(SystemExit) as excinfo:
        main((
            'autopep8-wrapper', 'autopep8',
            'https://github.com/pre-commit/mirrors-autopep8',
            '--foo', 'bar',
        ))
    msg, = excinfo.value.args
    assert msg == (
        '`autopep8-wrapper` has been removed -- '
        'use `autopep8` from https://github.com/pre-commit/mirrors-autopep8'
    )
