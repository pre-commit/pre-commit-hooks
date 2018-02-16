from __future__ import absolute_import
from __future__ import unicode_literals

from pre_commit_hooks.print_message import default_message
from pre_commit_hooks.print_message import main


def test_passes_by_default():
    assert main() == 0


def test_fails_with_fail_flag():
    assert main(['-f']) > 0
    assert main(['--f']) > 0


def test_default_message(capsys):
    main()
    stdout, _ = capsys.readouterr()
    assert stdout.strip() == default_message


def test_message_argument(capsys):
    message = 'a message'
    main(['-m', message])
    stdout, _ = capsys.readouterr()
    assert stdout.strip() == message
