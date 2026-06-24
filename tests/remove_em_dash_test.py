from __future__ import annotations

import pytest

from pre_commit_hooks.remove_em_dash import main


@pytest.mark.parametrize(
    ('text', 'expected'),
    (
        ('foo\N{EM DASH}bar\n', b'foo-bar\n'),
        ('foo \N{EM DASH} bar\n', b'foo - bar\n'),
        ('a\N{EM DASH}b\N{EM DASH}c\n', b'a-b-c\n'),
        ('x\N{EM DASH}y\r\nz\r\n', b'x-y\r\nz\r\n'),
    ),
)
def test_fixes_em_dash(text, expected, tmpdir):
    path = tmpdir.join('file.txt')
    path.write_binary(text.encode())
    assert main((str(path),)) == 1
    assert path.read_binary() == expected


@pytest.mark.parametrize(
    'contents',
    (
        pytest.param(b'foo-bar\n', id='plain-hyphen'),
        pytest.param(b'no em dashes here\n', id='no-dash'),
        pytest.param(b'<a>\x97</a>\n', id='windows-1252-em-dash'),
    ),
)
def test_noop_without_utf8_em_dash(contents, tmpdir):
    path = tmpdir.join('file.txt')
    path.write_binary(contents)
    assert main((str(path),)) == 0
    assert path.read_binary() == contents
