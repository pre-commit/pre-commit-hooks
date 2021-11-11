import pytest

from pre_commit_hooks.check_encoding import main


@pytest.mark.parametrize(
    ('content', 'encoding', 'expected'),
    (
        (b'Hello!', 'ascii', 0),
        (b'Hello!', 'unknown-encoding', 2),
        ('Hello ☃!'.encode(), 'ascii', 1),
    ),
)
def test_has_encoding(content, encoding, expected, tmpdir):
    path = tmpdir.join('path')
    path.write(content, 'wb')
    assert main(('--encoding', encoding, str(path))) == expected
