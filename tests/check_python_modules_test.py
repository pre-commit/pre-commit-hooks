import pytest

from pre_commit_hooks.check_python_modules import main


@pytest.mark.parametrize('has_init', (True, False))
def test_main(tmpdir, has_init):
    if has_init:
        tmpdir.join('__init__.py').ensure()
    path = tmpdir.join('thing.py').ensure()

    expected = 0 if has_init else 1
    assert main((path.strpath,)) == expected
