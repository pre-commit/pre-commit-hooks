import pytest

from pre_commit_hooks.file_contents_sorter import FAIL
from pre_commit_hooks.file_contents_sorter import main
from pre_commit_hooks.file_contents_sorter import PASS


@pytest.mark.parametrize(
    ('input_s', 'argv', 'expected_retval', 'output'),
    (
        (b'', [], FAIL, b'\n'),
        (b'lonesome\n', [], PASS, b'lonesome\n'),
        (b'missing_newline', [], FAIL, b'missing_newline\n'),
        (b'newline\nmissing', [], FAIL, b'missing\nnewline\n'),
        (b'missing\nnewline', [], FAIL, b'missing\nnewline\n'),
        (b'alpha\nbeta\n', [], PASS, b'alpha\nbeta\n'),
        (b'beta\nalpha\n', [], FAIL, b'alpha\nbeta\n'),
        (b'C\nc\n', [], PASS, b'C\nc\n'),
        (b'c\nC\n', [], FAIL, b'C\nc\n'),
        (b'mag ical \n tre vor\n', [], FAIL, b' tre vor\nmag ical \n'),
        (b'@\n-\n_\n#\n', [], FAIL, b'#\n-\n@\n_\n'),
        (b'extra\n\n\nwhitespace\n', [], FAIL, b'extra\nwhitespace\n'),
        (b'whitespace\n\n\nextra\n', [], FAIL, b'extra\nwhitespace\n'),
        (
            b'fee\nFie\nFoe\nfum\n',
            [],
            FAIL,
            b'Fie\nFoe\nfee\nfum\n',
        ),
        (
            b'Fie\nFoe\nfee\nfum\n',
            [],
            PASS,
            b'Fie\nFoe\nfee\nfum\n',
        ),
        (
            b'fee\nFie\nFoe\nfum\n',
            ['--ignore-case'],
            PASS,
            b'fee\nFie\nFoe\nfum\n',
        ),
        (
            b'Fie\nFoe\nfee\nfum\n',
            ['--ignore-case'],
            FAIL,
            b'fee\nFie\nFoe\nfum\n',
        ),
        (
            b'Fie\nFoe\nfee\nfee\nfum\n',
            ['--ignore-case'],
            FAIL,
            b'fee\nfee\nFie\nFoe\nfum\n',
        ),
        (
            b'Fie\nFoe\nfee\nfum\n',
            ['--unique'],
            PASS,
            b'Fie\nFoe\nfee\nfum\n',
        ),
        (
            b'Fie\nFie\nFoe\nfee\nfum\n',
            ['--unique'],
            FAIL,
            b'Fie\nFoe\nfee\nfum\n',
        ),
        (
            b'fee\nFie\nFoe\nfum\n',
            ['--unique', '--ignore-case'],
            PASS,
            b'fee\nFie\nFoe\nfum\n',
        ),
        (
            b'fee\nfee\nFie\nFoe\nfum\n',
            ['--unique', '--ignore-case'],
            FAIL,
            b'fee\nFie\nFoe\nfum\n',
        ),
    ),
)
def test_integration(input_s, argv, expected_retval, output, tmpdir):
    path = tmpdir.join('file.txt')
    path.write_binary(input_s)

    output_retval = main([str(path)] + argv)

    assert path.read_binary() == output
    assert output_retval == expected_retval
