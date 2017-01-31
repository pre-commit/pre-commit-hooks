import os
import shutil

import pytest

from pre_commit_hooks.pretty_format_yaml import pretty_format_yaml
from testing.util import get_resource_path


def get_yaml_resource_path(path):
    return get_resource_path(os.path.join('yaml_files', path))


@pytest.mark.parametrize(('filename', 'expected_retval'), (
    ('pretty_formatted_yaml.yaml', 0),
    ('not_pretty_formatted_yaml.yaml', 1),
))
def test_pretty_format_yaml(filename, expected_retval):
    ret = pretty_format_yaml([get_yaml_resource_path(filename)])
    assert ret == expected_retval


@pytest.mark.parametrize(('filename', 'arguments'), (
    ('pretty_formatted_yaml_default_style_True.yaml', '--default_style=True'),
    ('pretty_formatted_yaml_default_flow_style_False.yaml', '--default_flow_style=False'),
    ('pretty_formatted_yaml_canonical_True.yaml', '--canonical=True'),
    ('pretty_formatted_yaml_indent_4.yaml', '--indent=4'),
))
def test_pretty_format_yaml_arguments_success(filename, arguments):
    assert pretty_format_yaml(arguments.split() + [get_yaml_resource_path(filename)]) == 0


def test_autofix_pretty_format_yaml(tmpdir):
    srcfile = tmpdir.join('to_be_yaml_formatted.yaml')
    shutil.copyfile(
        get_yaml_resource_path('not_pretty_formatted_yaml.yaml'),
        srcfile.strpath,
    )

    # now launch the autofix on that file
    ret = pretty_format_yaml(['--autofix', srcfile.strpath])
    # it should have formatted it
    assert ret == 1

    # file was formatted (shouldn't trigger linter again)
    ret = pretty_format_yaml([srcfile.strpath])
    assert ret == 0


@pytest.mark.parametrize(('argument', 'value'), (
    ('--default_flow_style', 1),
    ('--canonical', 'wrong_value'),
    ('--indent', 'casual string'),
    ('--width', 'casual string'),
    ('--allow_unicode', 'no'),
    ('--line_break', 'nein'),
    ('--explicit_start', 'y'),
    ('--explicit_end', 'n'),

))
def test_pretty_format_yaml_wrong_arguments(argument, value):
    with pytest.raises(SystemExit):
        pretty_format_yaml([argument + '=' + str(value), get_yaml_resource_path('pretty_formatted_yaml')])


def test_pretty_format_yaml_invalid_yaml_file(tmpdir):
    invalid_yaml_file = tmpdir.join('invalid.yaml')
    with open(invalid_yaml_file.strpath, 'w') as invalid_yaml:
        invalid_yaml.write("""
foo: "bar"
alist:
2
34
234
blah: null
""")
    assert pretty_format_yaml([invalid_yaml_file.strpath]) == 1
