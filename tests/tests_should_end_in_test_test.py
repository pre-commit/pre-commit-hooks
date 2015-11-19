from pre_commit_hooks.tests_should_end_in_test import validate_files


def test_validate_files_all_pass():
    ret = validate_files(['foo_test.py', 'bar_test.py'])
    assert ret == 0


def test_validate_files_one_fails():
    ret = validate_files(['not_test_ending.py', 'foo_test.py'])
    assert ret == 1


def test_validate_files_django_all_pass():
    ret = validate_files(['--django', 'test_foo.py', 'test_bar.py', 'tests/test_baz.py'])
    assert ret == 0


def test_validate_files_django_one_fails():
    ret = validate_files(['--django', 'not_test_ending.py', 'test_foo.py'])
    assert ret == 1


def test_validate_nested_files_django_one_fails():
    ret = validate_files(['--django', 'tests/not_test_ending.py', 'test_foo.py'])
    assert ret == 1


def test_validate_files_not_django_fails():
    ret = validate_files(['foo_test.py', 'bar_test.py', 'test_baz.py'])
    assert ret == 1


def test_validate_files_django_fails():
    ret = validate_files(['--django', 'foo_test.py', 'test_bar.py', 'test_baz.py'])
    assert ret == 1
