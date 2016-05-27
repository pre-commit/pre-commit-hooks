from __future__ import absolute_import
from __future__ import unicode_literals

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
    path = tmpdir.join('test.py')
    path.write(input_src)
    ret = main([path.strpath, '-i', '-v'])
    assert ret == expected_ret
    assert path.read() == output_src


def test_respects_config_file(tmpdir):
    with tmpdir.as_cwd():
        tmpdir.join('setup.cfg').write('[pep8]\nignore=E221')
        tmpdir.join('test.py').write('print(1    + 2)\n')
        assert main(['test.py', '-i', '-v']) == 0
