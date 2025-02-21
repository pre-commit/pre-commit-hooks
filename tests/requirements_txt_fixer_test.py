from __future__ import annotations

import pytest

from pre_commit_hooks.requirements_txt_fixer import FAIL
from pre_commit_hooks.requirements_txt_fixer import main
from pre_commit_hooks.requirements_txt_fixer import PASS
from pre_commit_hooks.requirements_txt_fixer import Requirement


@pytest.mark.parametrize(
    ('input_s', 'expected_retval', 'output'),
    (
        (b'', PASS, b''),
        (b'\n', PASS, b'\n'),
        (b'# intentionally empty\n', PASS, b'# intentionally empty\n'),
        (b'foo\n# comment at end\n', PASS, b'foo\n# comment at end\n'),
        (b'foo\nbar\n', FAIL, b'bar\nfoo\n'),
        (b'bar\nfoo\n', PASS, b'bar\nfoo\n'),
        (b'a\nc\nb\n', FAIL, b'a\nb\nc\n'),
        (b'a\nc\nb', FAIL, b'a\nb\nc\n'),
        (b'a\nb\nc', FAIL, b'a\nb\nc\n'),
        (
            b'#comment1\nfoo\n#comment2\nbar\n',
            FAIL,
            b'#comment2\nbar\n#comment1\nfoo\n',
        ),
        (
            b'#comment1\nbar\n#comment2\nfoo\n',
            PASS,
            b'#comment1\nbar\n#comment2\nfoo\n',
        ),
        (b'#comment\n\nfoo\nbar\n', FAIL, b'#comment\n\nbar\nfoo\n'),
        (b'#comment\n\nbar\nfoo\n', PASS, b'#comment\n\nbar\nfoo\n'),
        (
            b'foo\n\t#comment with indent\nbar\n',
            FAIL,
            b'\t#comment with indent\nbar\nfoo\n',
        ),
        (
            b'bar\n\t#comment with indent\nfoo\n',
            PASS,
            b'bar\n\t#comment with indent\nfoo\n',
        ),
        (b'\nfoo\nbar\n', FAIL, b'bar\n\nfoo\n'),
        (b'\nbar\nfoo\n', PASS, b'\nbar\nfoo\n'),
        (
            b'pyramid-foo==1\npyramid>=2\n',
            FAIL,
            b'pyramid>=2\npyramid-foo==1\n',
        ),
        (
            b'a==1\n'
            b'c>=1\n'
            b'bbbb!=1\n'
            b'c-a>=1;python_version>="3.6"\n'
            b'e>=2\n'
            b'd>2\n'
            b'g<2\n'
            b'f<=2\n',
            FAIL,
            b'a==1\n'
            b'bbbb!=1\n'
            b'c>=1\n'
            b'c-a>=1;python_version>="3.6"\n'
            b'd>2\n'
            b'e>=2\n'
            b'f<=2\n'
            b'g<2\n',
        ),
        (b'a==1\nb==1\na==1\n', FAIL, b'a==1\nb==1\n'),
        (
            b'a==1\nb==1\n#comment about a\na==1\n',
            FAIL,
            b'#comment about a\na==1\nb==1\n',
        ),
        (b'ocflib\nDjango\nPyMySQL\n', FAIL, b'Django\nocflib\nPyMySQL\n'),
        (
            b'-e git+ssh://git_url@tag#egg=ocflib\nDjango\nPyMySQL\n',
            FAIL,
            b'Django\n-e git+ssh://git_url@tag#egg=ocflib\nPyMySQL\n',
        ),
        (b'bar\npkg-resources==0.0.0\nfoo\n', FAIL, b'bar\nfoo\n'),
        (b'foo\npkg-resources==0.0.0\nbar\n', FAIL, b'bar\nfoo\n'),
        (b'bar\npkg_resources==0.0.0\nfoo\n', FAIL, b'bar\nfoo\n'),
        (b'foo\npkg_resources==0.0.0\nbar\n', FAIL, b'bar\nfoo\n'),
        (
            b'git+ssh://git_url@tag#egg=ocflib\nDjango\nijk\n',
            FAIL,
            b'Django\nijk\ngit+ssh://git_url@tag#egg=ocflib\n',
        ),
        (
            b'b==1.0.0\n'
            b'c=2.0.0 \\\n'
            b' --hash=sha256:abcd\n'
            b'a=3.0.0 \\\n'
            b'  --hash=sha256:a1b1c1d1',
            FAIL,
            b'a=3.0.0 \\\n'
            b'  --hash=sha256:a1b1c1d1\n'
            b'b==1.0.0\n'
            b'c=2.0.0 \\\n'
            b' --hash=sha256:abcd\n',
        ),
        (
            b'a=2.0.0 \\\n --hash=sha256:abcd\nb==1.0.0\n',
            PASS,
            b'a=2.0.0 \\\n --hash=sha256:abcd\nb==1.0.0\n',
        ),
    ),
)
def test_integration(input_s, expected_retval, output, tmpdir):
    path = tmpdir.join('file.txt')
    path.write_binary(input_s)

    output_retval = main([str(path)])

    assert path.read_binary() == output
    assert output_retval == expected_retval


def test_requirement_object():
    top_of_file = Requirement()
    top_of_file.comments.append(b'#foo')
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
