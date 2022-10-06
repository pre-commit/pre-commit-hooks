from __future__ import annotations

import pytest

from pre_commit_hooks.string_fixer_for_jupyter_notebooks import main
from testing.util import get_resource_path


TESTS = (
    ('jupyter_case_1_before.ipynb', 'jupyter_case_1_after.ipynb', 1),
    # the file in Case 2 is not altered, so we reload the same file
    ('jupyter_case_2.ipynb', 'jupyter_case_2.ipynb', 0),
)


@pytest.mark.parametrize(('input_file', 'output_file', 'expected_retv'), TESTS)
def test_rewrite(input_file, output_file, expected_retv, tmpdir):
    with open(get_resource_path(input_file)) as f:
        before_contents = f.read()

    with open(get_resource_path(output_file)) as f:
        after_contents = f.read()

    path = tmpdir.join('file.ipynb')
    path.write(before_contents)
    retval = main([str(path)])
    assert path.read() == after_contents
    assert retval == expected_retv
