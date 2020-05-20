import io

import pytest

from pre_commit_hooks.fix_encoding_pragma import _normalize_pragma
from pre_commit_hooks.fix_encoding_pragma import fix_encoding_pragma
from pre_commit_hooks.fix_encoding_pragma import main


def test_integration_inserting_pragma(tmpdir):
    path = tmpdir.join('foo.py')
    path.write_binary(b'import httplib\n')

    assert main((str(path),)) == 1

    assert path.read_binary() == (
        b'# -*- coding: utf-8 -*-\n'
        b'import httplib\n'
    )


def test_integration_ok(tmpdir):
    path = tmpdir.join('foo.py')
    path.write_binary(b'# -*- coding: utf-8 -*-\nx = 1\n')
    assert main((str(path),)) == 0


def test_integration_remove(tmpdir):
    path = tmpdir.join('foo.py')
    path.write_binary(b'# -*- coding: utf-8 -*-\nx = 1\n')

    assert main((str(path), '--remove')) == 1

    assert path.read_binary() == b'x = 1\n'


def test_integration_remove_ok(tmpdir):
    path = tmpdir.join('foo.py')
    path.write_binary(b'x = 1\n')
    assert main((str(path), '--remove')) == 0


@pytest.mark.parametrize(
    'input_str',
    (
        b'',
        (
            b'# -*- coding: utf-8 -*-\n'
            b'x = 1\n'
        ),
        (
            b'#!/usr/bin/env python\n'
            b'# -*- coding: utf-8 -*-\n'
            b'foo = "bar"\n'
        ),
    ),
)
def test_ok_inputs(input_str):
    bytesio = io.BytesIO(input_str)
    assert fix_encoding_pragma(bytesio) == 0
    bytesio.seek(0)
    assert bytesio.read() == input_str


@pytest.mark.parametrize(
    ('input_str', 'output'),
    (
        (
            b'import httplib\n',
            b'# -*- coding: utf-8 -*-\n'
            b'import httplib\n',
        ),
        (
            b'#!/usr/bin/env python\n'
            b'x = 1\n',
            b'#!/usr/bin/env python\n'
            b'# -*- coding: utf-8 -*-\n'
            b'x = 1\n',
        ),
        (
            b'#coding=utf-8\n'
            b'x = 1\n',
            b'# -*- coding: utf-8 -*-\n'
            b'x = 1\n',
        ),
        (
            b'#!/usr/bin/env python\n'
            b'#coding=utf8\n'
            b'x = 1\n',
            b'#!/usr/bin/env python\n'
            b'# -*- coding: utf-8 -*-\n'
            b'x = 1\n',
        ),
        # These should each get truncated
        (b'#coding: utf-8\n', b''),
        (b'# -*- coding: utf-8 -*-\n', b''),
        (b'#!/usr/bin/env python\n', b''),
        (b'#!/usr/bin/env python\n#coding: utf8\n', b''),
        (b'#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n', b''),
    ),
)
def test_not_ok_inputs(input_str, output):
    bytesio = io.BytesIO(input_str)
    assert fix_encoding_pragma(bytesio) == 1
    bytesio.seek(0)
    assert bytesio.read() == output


def test_ok_input_alternate_pragma():
    input_s = b'# coding: utf-8\nx = 1\n'
    bytesio = io.BytesIO(input_s)
    ret = fix_encoding_pragma(bytesio, expected_pragma=b'# coding: utf-8')
    assert ret == 0
    bytesio.seek(0)
    assert bytesio.read() == input_s


def test_not_ok_input_alternate_pragma():
    bytesio = io.BytesIO(b'x = 1\n')
    ret = fix_encoding_pragma(bytesio, expected_pragma=b'# coding: utf-8')
    assert ret == 1
    bytesio.seek(0)
    assert bytesio.read() == b'# coding: utf-8\nx = 1\n'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('# coding: utf-8', b'# coding: utf-8'),
        # trailing whitespace
        ('# coding: utf-8\n', b'# coding: utf-8'),
    ),
)
def test_normalize_pragma(input_s, expected):
    assert _normalize_pragma(input_s) == expected


def test_integration_alternate_pragma(tmpdir, capsys):
    f = tmpdir.join('f.py')
    f.write('x = 1\n')

    pragma = '# coding: utf-8'
    assert main((str(f), '--pragma', pragma)) == 1
    assert f.read() == '# coding: utf-8\nx = 1\n'
    out, _ = capsys.readouterr()
    assert out == f'Added `# coding: utf-8` to {str(f)}\n'


def test_crlf_ok(tmpdir):
    f = tmpdir.join('f.py')
    f.write_binary(b'# -*- coding: utf-8 -*-\r\nx = 1\r\n')
    assert not main((str(f),))


def test_crfl_adds(tmpdir):
    f = tmpdir.join('f.py')
    f.write_binary(b'x = 1\r\n')
    assert main((str(f),))
    assert f.read_binary() == b'# -*- coding: utf-8 -*-\r\nx = 1\r\n'
