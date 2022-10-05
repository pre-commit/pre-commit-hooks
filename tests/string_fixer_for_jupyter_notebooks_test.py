from pre_commit_hooks.string_fixer_for_jupyter_notebooks import main
from testing.util import get_resource_path


def test_rewrite(tmpdir):
    with open(get_resource_path('before.ipynb')) as f:
        before_contents = f.read()

    with open(get_resource_path('after.ipynb')) as f:
        after_contents = f.read()

    path = tmpdir.join('file.ipynb')
    path.write(before_contents)
    retval = main([str(path)])
    assert path.read() == after_contents
    assert retval == 1
