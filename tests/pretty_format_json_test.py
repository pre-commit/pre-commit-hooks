import tempfile

import pytest

from pre_commit_hooks.pretty_format_json import pretty_format_json
from testing.util import get_resource_path


@pytest.mark.parametrize(('filename', 'expected_retval'), (
    ('not_pretty_formatted_json.json', 1),
    ('pretty_formatted_json.json', 0),
))
def test_pretty_format_json(filename, expected_retval):
    ret = pretty_format_json([get_resource_path(filename)])
    assert ret == expected_retval


def test_autofix_pretty_format_json():
    toformat_file = tempfile.NamedTemporaryFile(delete=False, mode='w+')

    # copy our file to format there
    model_file = open(get_resource_path('not_pretty_formatted_json.json'), 'r')
    model_contents = model_file.read()
    model_file.close()

    toformat_file.write(model_contents)
    toformat_file.close()

    # now launch the autofix on that file
    ret = pretty_format_json(['--autofix', toformat_file.name])
    # it should have formatted it
    assert ret == 1

    # file already good
    ret = pretty_format_json([toformat_file.name])
    assert ret == 0


def test_badfile_pretty_format_json():
    ret = pretty_format_json([get_resource_path('ok_yaml.yaml')])
    assert ret == 1
