from __future__ import annotations

import os

import yaml

from pre_commit_hooks.check_yaml_sorted import is_sorted
from pre_commit_hooks.check_yaml_sorted import main


def test_sort_list_by_items():
    assert is_sorted(['a'])
    assert is_sorted(['a', 'b'])
    assert not is_sorted(['b', 'a'])
    assert is_sorted(['a', 'b', 'c', 'd'])
    assert not is_sorted(['a', 'b', 'd', 'c'])


def test_sort_dicts_by_keys():
    assert is_sorted({'a': 1, 'b': ['nested', 'list'], 'c': 3})
    assert not is_sorted({'a': 1, 'c': ['nested', 'list'], 'b': 3})


_list_dicts_first_key_sorted = """
-   first_dict:
        some: stuff
-   second_dict:
        other: stuff
-   third_dict:
        even: more stuff
"""

_list_dicts_first_key_unsorted = """
-   second_dict:
        some: stuff
-   first_dict:
        other: stuff
-   third_dict:
        even: more stuff
"""


def test_sort_list_of_dicts_by_first_key():
    assert is_sorted(yaml.safe_load(_list_dicts_first_key_sorted))
    assert not is_sorted(yaml.safe_load(_list_dicts_first_key_unsorted))


_sorted_yaml = """
-   id: check-builtin-literals
-   id: check-case-conflict
-   id: check-docstring-first
"""

_sorted_yaml_long = """
-   id: check-builtin-literals
    name: check builtin type constructor use
    description: requires literal syntax when initializing empty or zero....
    entry: check-builtin-literals
    language: python
    types: [python]
-   id: check-case-conflict
    name: check for case conflicts
    description: checks for files that would conflict in case-insensitive...
    entry: check-case-conflict
    language: python
-   id: check-docstring-first
    name: check docstring is first
    description: checks a common error of defining a docstring after code.
    entry: check-docstring-first
    language: python
    types: [python]
"""

_unsorted_yaml = """
-   id: check-builtin-literals
-   id: check-docstring-first
-   id: check-case-conflict
"""

_unsorted_yaml_long = """
-   id: check-builtin-literals
    name: check builtin type constructor use
    description: requires literal syntax when initializing empty or zero....
    entry: check-builtin-literals
    language: python
    types: [python]
-   id: check-docstring-first
    name: check docstring is first
    description: checks a common error of defining a docstring after code.
    entry: check-docstring-first
    language: python
    types: [python]
-   id: check-case-conflict
    name: check for case conflicts
    description: checks for files that would conflict in case-insensitive...
    entry: check-case-conflict
    language: python
"""


def test_sort_list_of_dicts_same_first_key_by_val():
    assert is_sorted(yaml.safe_load(_sorted_yaml))
    assert is_sorted(yaml.safe_load(_sorted_yaml_long))
    assert not is_sorted(yaml.safe_load(_unsorted_yaml))
    assert not is_sorted(yaml.safe_load(_unsorted_yaml_long))


def test_integration(tmpdir):
    file_path = os.path.join(str(tmpdir), 'foo.yaml')

    with open(file_path, 'w') as f:
        f.write(_sorted_yaml)

    assert main([file_path]) == 0

    with open(file_path, 'w') as f:
        f.write(_unsorted_yaml)

    assert main([file_path]) != 0
