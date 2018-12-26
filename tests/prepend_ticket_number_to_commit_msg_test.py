from __future__ import absolute_import
from __future__ import unicode_literals

import mock
import pytest
import six

from pre_commit_hooks.prepend_ticket_number_to_commit_msg import get_branch_name
from pre_commit_hooks.prepend_ticket_number_to_commit_msg import main
from pre_commit_hooks.prepend_ticket_number_to_commit_msg import update_commit_message


TESTING_MODULE = 'pre_commit_hooks.prepend_ticket_number_to_commit_msg'


@pytest.mark.parametrize(
    ('msg'),
    (
        'Test',
        'JIRA-1234_Test',
    ),
)
@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message(mock_branch_name, msg, tmpdir):
    mock_branch_name.return_value = 'JIRA-1234_new_feature'
    path = tmpdir.join('file.txt')
    path.write(msg)
    update_commit_message(six.text_type(path), '[A-Z]+-\d+')  # noqa
    assert 'JIRA-1234' in path.read()


@mock.patch(TESTING_MODULE + '.subprocess')
def test_get_branch_name(mock_subprocess):
    get_branch_name()
    mock_subprocess.check_output.assert_called_once_with(
        [
            'git',
            'rev-parse',
            '--abbrev-ref',
            'HEAD',
        ],
    )


@mock.patch(TESTING_MODULE + '.argparse')
@mock.patch(TESTING_MODULE + '.update_commit_message')
def test_main(mock_update_commit_message, mock_argparse):
    mock_args = mock.Mock()
    mock_args.filenames = ['foo.txt']
    mock_args.regex = None
    mock_argparse.ArgumentParser.return_value.parse_args.return_value = mock_args
    main()
    mock_update_commit_message.assert_called_once_with('foo.txt', '[A-Z]+-\d+')  # noqa
