import os.path

import pytest

from pre_commit_hooks.requirements_txt_fixer import fix_requirements_txt
from pre_commit_hooks.requirements_txt_fixer import Requirement

# Input, expected return value, expected output
TESTS = (
    (b'foo\nbar\n', 1, b'bar\nfoo\n'),
    (b'bar\nfoo\n', 0, b'bar\nfoo\n'),
    (b'#comment1\nfoo\n#comment2\nbar\n', 1, b'#comment2\nbar\n#comment1\nfoo\n'),
    (b'#comment1\nbar\n#comment2\nfoo\n', 0, b'#comment1\nbar\n#comment2\nfoo\n'),
    (b'#comment\n\nfoo\nbar\n', 1, b'#comment\n\nbar\nfoo\n'),
    (b'#comment\n\nbar\nfoo\n', 0, b'#comment\n\nbar\nfoo\n'),
    (b'\nfoo\nbar\n', 1, b'bar\n\nfoo\n'),
    (b'\nbar\nfoo\n', 0, b'\nbar\nfoo\n'),
    (b'pyramid==1\npyramid-foo==2\n', 0, b'pyramid==1\npyramid-foo==2\n'),
    (b'ocflib\nDjango\nPyMySQL\n', 1, b'Django\nocflib\nPyMySQL\n'),
)


@pytest.mark.parametrize(('input_s', 'expected_retval', 'output'), TESTS)
def test_integration(input_s, expected_retval, output, tmpdir):
    path = os.path.join(tmpdir.strpath, 'file.txt')

    with open(path, 'wb') as file_obj:
        file_obj.write(input_s)

    assert fix_requirements_txt([path]) == expected_retval
    assert open(path, 'rb').read() == output


def test_requirement_object():
    top_of_file = Requirement()
    top_of_file.comments.append('#foo')
    top_of_file.value = b'\n'

    requirement_foo = Requirement()
    requirement_foo.value = b'foo'

    requirement_bar = Requirement()
    requirement_bar.value = b'bar'

    # This may look redundant, but we need to test both foo.__lt__(bar) and
    # bar.__lt__(foo)
    assert requirement_foo > top_of_file
    assert top_of_file < requirement_foo
    assert requirement_foo > requirement_bar
    assert requirement_bar < requirement_foo
