from __future__ import absolute_import
from __future__ import unicode_literals

import io

import pytest

from pre_commit_hooks.fix_encoding_pragma import fix_encoding_pragma
from pre_commit_hooks.fix_encoding_pragma import main


def test_integration_inserting_pragma(tmpdir):
    path = tmpdir.join('foo.py')
    path.write_binary(b'import httplib\n')

    assert main((path.strpath,)) == 1

    assert path.read_binary() == (
        b'# -*- coding: utf-8 -*-\n'
        b'import httplib\n'
    )


def test_integration_ok(tmpdir):
    path = tmpdir.join('foo.py')
    path.write_binary(b'# -*- coding: utf-8 -*-\nx = 1\n')
    assert main((path.strpath,)) == 0


def test_integration_remove(tmpdir):
    path = tmpdir.join('foo.py')
    path.write_binary(b'# -*- coding: utf-8 -*-\nx = 1\n')

    assert main((path.strpath, '--remove')) == 1

    assert path.read_binary() == b'x = 1\n'


def test_integration_remove_ok(tmpdir):
    path = tmpdir.join('foo.py')
    path.write_binary(b'x = 1\n')
    assert main((path.strpath, '--remove')) == 0


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
    )
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
    )
)
def test_not_ok_inputs(input_str, output):
    bytesio = io.BytesIO(input_str)
    assert fix_encoding_pragma(bytesio) == 1
    bytesio.seek(0)
    assert bytesio.read() == output
