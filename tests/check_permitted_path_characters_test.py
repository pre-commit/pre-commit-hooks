from __future__ import annotations

from pre_commit_hooks.check_permitted_path_characters import main


def test_main_all_pass():
    ret = main(
        [
            '/some/path/foo_test.py',
            './relative/path/bar_test.py',
            'filename-only.py',
        ],
    )
    assert ret == 0


def test_main_default_chars():
    # use '--' for separating pathnames from args, so pathnames with leading
    # '-' are not interpreted as flags
    ret = main(
        [
            '--',
            '-.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_',
            'abcdefghijklmnopqrstuvwxyz',
        ],
    )
    assert ret == 0

    ret = main(['+'])
    assert ret == 1


def test_main_invalid_dir():
    ret = main(['--', '/some+funky%%dir/pathname'])
    assert ret == 1


def test_main_allowlist():
    ret = main(['--allowlist', 'abc', 'invalid.py'])
    assert ret == 1
    ret = main(['--allowlist', 'abc', 'cba'])
    assert ret == 0
    # a pathological case
    ret = main(['--allowlist', '\b\x01\t/.', '\b.\x01/\t'])
    assert ret == 0


def test_main_extra_allowlist():
    ret = main(['--extra-allowlist', '+', 'valid+'])
    assert ret == 0
