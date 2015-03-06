[![Build Status](https://travis-ci.org/pre-commit/pre-commit-hooks.svg?branch=master)](https://travis-ci.org/pre-commit/pre-commit-hooks)
[![Coverage Status](https://img.shields.io/coveralls/pre-commit/pre-commit-hooks.svg?branch=master)](https://coveralls.io/r/pre-commit/pre-commit-hooks)
[![Build status](https://ci.appveyor.com/api/projects/status/dfcpng35u4g0r0t1/branch/master?svg=true)](https://ci.appveyor.com/project/asottile/pre-commit-hooks/branch/master)

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

- `autopep8-wrapper` - Runs autopep8 over python source. (You'll want `args: ['-i]` when using this hook, see `.pre-commit-config.yaml` for an example.)
- `check-added-large-files` - Prevent giant files from being committed.
- `check-case-conflict` - Check for files that would conflict in case-insensitive filesystems.
- `check-docstring-first` - Checks a common error of defining a docstring after code.
- `check-json` - Attempts to load all json files to verify syntax.
- `check-xml` - Attempts to load all xml files to verify syntax.
- `check-yaml` - Attempts to load all yaml files to verify syntax.
- `debug-statements` - Check for pdb / ipdb / pudb statements in code.
- `detect-private-key` - Checks for the existence of private keys
- `double-quote-string-fixer` - This hook replaces double quoted strings with single quoted strings
- `end-of-file-fixer` - Makes sure files end in a newline and only a newline.
- `flake8` - Run flake8 on your python files
- `name-tests-test` - Assert that files in tests/ end in _test.py
- `pyflakes` - Run pyflakes on your python files
- `requirements-txt-fixer` - Sorts entries in requirements.txt
- `trailing-whitespace` - Trims trailing whitespace.

### As a standalone package

If you'd like to use these hooks, they're also available as a standalone
package.

Simply `pip install pre-commit-hooks`
