from pre_commit_hooks.tests_should_end_in_test import main


def test_main_all_pass():
    ret = main(['foo_test.py', 'bar_test.py'])
    assert ret == 0


def test_main_one_fails():
    ret = main(['not_test_ending.py', 'foo_test.py'])
    assert ret == 1


def test_regex():
    assert main(('foo_test_py',)) == 1


def test_main_django_all_pass():
    ret = main((
        '--django', 'tests.py', 'test_foo.py', 'test_bar.py',
        'tests/test_baz.py',
    ))
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
