[![Build Status](https://travis-ci.org/pre-commit/pre-commit-hooks.svg?branch=master)](https://travis-ci.org/pre-commit/pre-commit-hooks)
[![Coverage Status](https://img.shields.io/coveralls/pre-commit/pre-commit-hooks.svg?branch=master)](https://coveralls.io/r/pre-commit/pre-commit-hooks)

pre-commit-hooks
==========

Some out-of-the-box hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit


### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

    -   repo: git://github.com/pre-commit/pre-commit-hooks
        sha: ''  # Use the sha you want to point at
        hooks:
        -   id: trailing-whitespace
        # -   id: ...


### Hooks available

- `check-yaml` - Attempts to load all yaml files to verify syntax.
- `debug-statements` - Check for pdb / ipdb / pudb statements in code.
- `end-of-file-fixer` - Makes sure files end in a newline and only a newline.
- `flake8` - Run flake8 on your python files
- `name-tests-test` - Assert that files in tests/ end in _test.py
- `pyflakes` - Run pyflakes on your python files
- `trailing-whitespace` - Trims trailing whitespace.

### As a standalone package

If you'd like to use these hooks, they're also available as a standalone
package.

Simply `pip install pre-commit-hooks`
