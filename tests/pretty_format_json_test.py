import io

import pytest

from pre_commit_hooks.pretty_format_json import pretty_format_json
from testing.util import get_resource_path


@pytest.mark.parametrize(('filename', 'expected_retval'), (
    ('not_pretty_formatted_json.json', 1),
    ('unsorted_pretty_formatted_json.json', 1),
    ('pretty_formatted_json.json', 0),
))
def test_pretty_format_json(filename, expected_retval):
    ret = pretty_format_json([get_resource_path(filename)])
    assert ret == expected_retval


@pytest.mark.parametrize(('filename', 'expected_retval'), (
    ('not_pretty_formatted_json.json', 1),
    ('unsorted_pretty_formatted_json.json', 0),
    ('pretty_formatted_json.json', 0),
))
def test_unsorted_pretty_format_json(filename, expected_retval):
    ret = pretty_format_json(['--no-sort-keys', get_resource_path(filename)])
    assert ret == expected_retval


def test_autofix_pretty_format_json(tmpdir):
    srcfile = tmpdir.join('to_be_json_formatted.json')
    with io.open(get_resource_path('not_pretty_formatted_json.json')) as f:
        srcfile.write_text(f.read(), 'UTF-8')

    # now launch the autofix on that file
    ret = pretty_format_json(['--autofix', srcfile.strpath])
    # it should have formatted it
    assert ret == 1

    # file was formatted (shouldn't trigger linter again)
    ret = pretty_format_json([srcfile.strpath])
    assert ret == 0


def test_badfile_pretty_format_json():
    ret = pretty_format_json([get_resource_path('ok_yaml.yaml')])
    assert ret == 1
