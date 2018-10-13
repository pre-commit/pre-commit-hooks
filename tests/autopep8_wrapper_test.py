from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from pre_commit_hooks.autopep8_wrapper import main


def test_invariantly_fails():
    with pytest.raises(SystemExit) as excinfo:
        main()
    msg, = excinfo.value.args
    assert 'https://github.com/pre-commit/mirrors-autopep8' in msg
