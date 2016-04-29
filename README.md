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

- `auto-indent` - Checks and fixes indentation of function calls.
- `autopep8-wrapper` - Runs autopep8 over python source.
    - Ignore PEP 8 violation types with `args: ['-i', '--ignore=E000,...']` or
      through configuration of the `[pep8]` section in setup.cfg / tox.ini.
- `check-added-large-files` - Prevent giant files from being committed.
    - Specify what is "too large" with `args: ['--maxkb=123']` (default=500kB).
- `check-ast` - Simply check whether files parse as valid python.
- `check-byte-order-marker` - Forbid files which have a UTF-8 byte-order marker
- `check-case-conflict` - Check for files with names that would conflict on a
  case-insensitive filesystem like MacOS HFS+ or Windows FAT.
- `check-docstring-first` - Checks for a common error of placing code before
  the docstring.
- `check-json` - Attempts to load all json files to verify syntax.
- `check-merge-conflict` - Check for files that contain merge conflict strings.
- `check-symlinks` - Checks for symlinks which do not point to anything.
- `check-xml` - Attempts to load all xml files to verify syntax.
- `check-yaml` - Attempts to load all yaml files to verify syntax.
- `debug-statements` - Check for pdb / ipdb / pudb statements in code.
- `detect-aws-credentials` - Checks for the existence of AWS secrets that you have set up with the AWS CLI.
- `detect-private-key` - Checks for the existence of private keys.
- `double-quote-string-fixer` - This hook replaces double quoted strings
  with single quoted strings.
- `end-of-file-fixer` - Makes sure files end in a newline and only a newline.
- `fix-encoding-pragma` - Add `# -*- coding: utf-8 -*-` to the top of python files.
    - To remove the coding pragma pass `--remove` (useful in a python3-only codebase)
- `flake8` - Run flake8 on your python files.
- `name-tests-test` - Assert that files in tests/ end in `_test.py`.
    - Use `args: ['--django']` to match `test*.py` instead.
- `pyflakes` - Run pyflakes on your python files.
- `pretty-format-json` - Checks that all your JSON files are pretty
    - Use `args: ['--autofix']` to automatically fixing the encountered not-pretty-formatted files and
    `args: ['--no-sort-keys']` to disable the sort on the keys.
- `requirements-txt-fixer` - Sorts entries in requirements.txt
- `trailing-whitespace` - Trims trailing whitespace.
    - Markdown linebreak trailing spaces preserved for `.md` and`.markdown`;
      use `args: ['--markdown-linebreak-ext=txt,text']` to add other extensions,
      `args: ['--markdown-linebreak-ext=*']` to preserve them for all files,
      or `args: ['--no-markdown-linebreak-ext']` to disable and always trim.

### As a standalone package

If you'd like to use these hooks, they're also available as a standalone
package.

Simply `pip install pre-commit-hooks`
