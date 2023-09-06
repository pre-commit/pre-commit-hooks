from __future__ import annotations

import pytest

from pre_commit_hooks.detect_secret_token import main


@pytest.mark.parametrize(
    ('input', 'expected'),
    (
        pytest.param(
            'There is no secret here',
            0,
            id='no secret-token',
        ),
        pytest.param(
            'There is no secret here ☃',
            0,
            id='no secret-token unicode',
        ),
        pytest.param(
            'Read about using "secret-token:" in RFC 8959',
            0,
            id='has secret-token prefix only',
        ),
        pytest.param(
            'secret-token:E92FB7EB-D882-47A4-A265-A0B6135DC842%20foo',
            1,
            id='has secret-token',
        ),
    ),
)
def test_main(input, expected, tmpdir):
    path = tmpdir.join('file.txt')
    path.write(input)
    assert main([str(path)]) == expected
