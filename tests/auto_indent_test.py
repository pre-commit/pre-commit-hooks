# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import filecmp
import os
import sys
from shutil import copyfile

import pytest

from pre_commit_hooks.auto_indent import main
from pre_commit_hooks.auto_indent import RETURN_CODE
from testing.util import get_resource_path


def _has_ast_arg_lineno_support():
    """Checks if AST has all the info necessary to auto indent.

    Some Python implementations removed line numbers from AST arg objects and
    as a result we can't automatically format function calls.
    """
    if sys.version_info.major == 3 and sys.version_info.minor == 3:
        return False
    elif sys.version_info.major == 3 and sys.version_info.minor == 2:
        return False
    else:
        return True


@pytest.mark.parametrize(
    ('infile', 'expected_rc'),
    (
        ('file_with_acceptable_indentation', RETURN_CODE['no_change']),
        ('syntax_error', RETURN_CODE['syntax_error']),
    )
)
def test_check_indentation(infile, expected_rc):
    in_path = get_resource_path(os.path.join('auto_indent', infile))
    assert main([in_path]) == expected_rc


@pytest.mark.skipif(not _has_ast_arg_lineno_support(), reason='See docstring.')
def test_fix_bad_indentation(tmpdir):
    in_path = get_resource_path(os.path.join(
        'auto_indent',
        'file_with_bad_indentation'
    ))
    expected_out_path = get_resource_path(os.path.join(
        'auto_indent',
        'file_with_acceptable_indentation'
    ))
    tmp_path = tmpdir.join('auto_indent').strpath
    copyfile(in_path, tmp_path)

    assert main([tmp_path]) == RETURN_CODE['fixed_file']
    assert filecmp.cmp(tmp_path, expected_out_path)


@pytest.mark.skipif(_has_ast_arg_lineno_support(), reason='See docstring.')
def test_partial_fix_bad_indentation(tmpdir):
    in_path = get_resource_path(os.path.join(
        'auto_indent',
        'file_with_bad_indentation'
    ))
    expected_out_path = get_resource_path(os.path.join(
        'auto_indent',
        'file_with_partial_indentation'
    ))
    tmp_path = tmpdir.join('auto_indent').strpath
    copyfile(in_path, tmp_path)

    assert main([tmp_path]) == RETURN_CODE['fixed_file']
    assert filecmp.cmp(tmp_path, expected_out_path)
