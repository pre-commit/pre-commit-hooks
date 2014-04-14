from pre_commit_hooks.tests_should_end_in_test import validate_files


def test_validate_files_all_pass():
    ret = validate_files(['foo_test.py', 'bar_test.py'])
    assert ret == 0


def test_validate_files_one_fails():
    ret = validate_files(['not_test_ending.py', 'foo_test.py'])
    assert ret == 1
