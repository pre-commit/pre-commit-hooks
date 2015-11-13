from __future__ import absolute_import
from __future__ import unicode_literals

import io

import pytest

from pre_commit_hooks.fix_encoding_pragma import fix_encoding_pragma
from pre_commit_hooks.fix_encoding_pragma import main


def test_integration_inserting_pragma(tmpdir):
    file_path = tmpdir.join('foo.py').strpath

    with open(file_path, 'wb') as file_obj:
        file_obj.write(b'import httplib\n')

    assert main([file_path]) == 1

    with open(file_path, 'rb') as file_obj:
        assert file_obj.read() == (
            b'# -*- coding: utf-8 -*-\n'
            b'import httplib\n'
        )


def test_integration_ok(tmpdir):
    file_path = tmpdir.join('foo.py').strpath
    with open(file_path, 'wb') as file_obj:
        file_obj.write(b'# -*- coding: utf-8 -*-\nx = 1\n')
    assert main([file_path]) == 0


@pytest.mark.parametrize(
    'input_str',
    (
        b'',
        b'# -*- coding: utf-8 -*-\n',
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
            b'#!/usr/bin/env python\n',
            b'#!/usr/bin/env python\n'
            b'# -*- coding: utf-8 -*-\n'
        ),
        (
            b'#coding=utf-8\n',
            b'# -*- coding: utf-8 -*-\n'
        ),
        (
            b'#!/usr/bin/env python\n'
            b'#coding=utf8\n',
            b'#!/usr/bin/env python\n'
            b'# -*- coding: utf-8 -*-\n',
        ),
    )
)
def test_not_ok_inputs(input_str, output):
    bytesio = io.BytesIO(input_str)
    assert fix_encoding_pragma(bytesio) == 1
    bytesio.seek(0)
    assert bytesio.read() == output
