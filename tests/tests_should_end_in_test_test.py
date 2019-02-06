from pre_commit_hooks.tests_should_end_in_test import main


def test_main_all_pass():
    ret = main(['foo_test.py', 'bar_test.py'])
    assert ret == 0


def test_main_one_fails():
    ret = main(['not_test_ending.py', 'foo_test.py'])
    assert ret == 1


def test_main_django_all_pass():
    ret = main(['--django', 'tests.py', 'test_foo.py', 'test_bar.py', 'tests/test_baz.py'])
    assert ret == 0


def test_main_django_one_fails():
    ret = main(['--django', 'not_test_ending.py', 'test_foo.py'])
    assert ret == 1


def test_validate_nested_files_django_one_fails():
    ret = main(['--django', 'tests/not_test_ending.py', 'test_foo.py'])
    assert ret == 1


def test_main_not_django_fails():
    ret = main(['foo_test.py', 'bar_test.py', 'test_baz.py'])
    assert ret == 1


def test_main_django_fails():
    ret = main(['--django', 'foo_test.py', 'test_bar.py', 'test_baz.py'])
    assert ret == 1


def test_exclude_default_factory_files():
    ret = main(['--django', 'test_bar.py', 'test_baz.py', 'factory.py', 'factories.py'])
    assert ret == 0


def test_exclude_custom_files_files():
    ret = main(['--django', '--exclude=tty.*.py', 'test_bar.py', 'test_baz.py', 'tty124.py', 'tty_file.py'])
    assert ret == 0


def test_exclude_no_match_files():
    ret = main(['--django', 'test_bar.py', 'test_baz.py', 'tty_file.py'])
    assert ret == 1
