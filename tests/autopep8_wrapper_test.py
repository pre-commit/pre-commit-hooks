from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os.path
import pytest

from pre_commit_hooks.autopep8_wrapper import main


@pytest.mark.parametrize(
    ('input_src', 'expected_ret', 'output_src'),
    (
        ('print(1    + 2)\n', 1, 'print(1 + 2)\n'),
        ('print(1 + 2)\n', 0, 'print(1 + 2)\n'),
    ),
)
def test_main_failing(tmpdir, input_src, expected_ret, output_src):
    filename = os.path.join(tmpdir.strpath, 'test.py')
    with io.open(filename, 'w') as file_obj:
        file_obj.write(input_src)
    ret = main([filename, '-i', '-v'])
    assert ret == expected_ret
    assert io.open(filename).read() == output_src
