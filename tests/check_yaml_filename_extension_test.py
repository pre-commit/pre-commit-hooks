from __future__ import annotations

import pytest

from pre_commit_hooks.check_yaml_filename_extension import main
from pre_commit_hooks.util import cmd_output


@pytest.mark.parametrize(
    ('filename', 'new_filename', 'expected_retval'), (
        ('file_1.yml', 'file_1.yaml', 1),
        ('.file_2.yml', '.file_2.yaml', 1),
        ('file_3.yaml', 'file_3.yaml', 0),
    ),
)
def test_main(temp_git_dir, filename, new_filename, expected_retval):
    with temp_git_dir.as_cwd():
        temp_git_dir.join(filename).write('---')
        cmd_output('git', 'add', filename)

        retv = main([filename])

        assert retv == expected_retval
        assert temp_git_dir.join(new_filename).exists()

        assert retv == 0 or not temp_git_dir.join(filename).exists()
