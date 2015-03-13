import os.path

import pytest

from pre_commit_hooks.check_merge_conflict import detect_merge_conflict

# Input, expected return value
TESTS = (
    (b'<<<<<<< HEAD', 1),
    (b'=======', 1),
    (b'>>>>>>> master', 1),
    (b'# <<<<<<< HEAD', 0),
    (b'# =======', 0),
    (b'import my_module', 0),
    (b'', 0),
)


@pytest.mark.parametrize(('input_s', 'expected_retval'), TESTS)
def test_detect_merge_conflict(input_s, expected_retval, tmpdir):
    path = os.path.join(tmpdir.strpath, 'file.txt')

    with open(path, 'wb') as file_obj:
        file_obj.write(input_s)

    assert detect_merge_conflict([path]) == expected_retval
