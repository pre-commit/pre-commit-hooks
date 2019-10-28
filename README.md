[![Build Status](https://asottile.visualstudio.com/asottile/_apis/build/status/pre-commit.pre-commit-hooks?branchName=master)](https://asottile.visualstudio.com/asottile/_build/latest?definitionId=17&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/17/master.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=17&branchName=master)

pre-commit-hooks
================

Some out-of-the-box hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit


### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

    -   repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v2.4.0  # Use the ref you want to point at
        hooks:
        -   id: trailing-whitespace
        # -   id: ...


### Hooks available

- `check-added-large-files` - Prevent giant files from being committed.
    - Specify what is "too large" with `args: ['--maxkb=123']` (default=500kB).
    - If `git-lfs` is installed, lfs files will be skipped
      (requires `git-lfs>=2.2.1`)
- `check-ast` - Simply check whether files parse as valid python.
- `check-builtin-literals` - Require literal syntax when initializing empty or zero Python builtin types.
    - Allows calling constructors with positional arguments (e.g., `list('abc')`).
    - Allows calling constructors from the `builtins` (`__builtin__`) namespace (`builtins.list()`).
    - Ignore this requirement for specific builtin types with `--ignore=type1,type2,…`.
    - Forbid `dict` keyword syntax with `--no-allow-dict-kwargs`.
- `check-byte-order-marker` - Forbid files which have a UTF-8 byte-order marker
- `check-case-conflict` - Check for files with names that would conflict on a
  case-insensitive filesystem like MacOS HFS+ or Windows FAT.
- `check-docstring-first` - Checks for a common error of placing code before
  the docstring.
- `check-executables-have-shebangs` - Checks that non-binary executables have a
  proper shebang.
- `check-json` - Attempts to load all json files to verify syntax.
- `check-merge-conflict` - Check for files that contain merge conflict strings.
- `check-symlinks` - Checks for symlinks which do not point to anything.
- `check-toml` - Attempts to load all TOML files to verify syntax.
- `check-vcs-permalinks` - Ensures that links to vcs websites are permalinks.
- `check-xml` - Attempts to load all xml files to verify syntax.
- `check-yaml` - Attempts to load all yaml files to verify syntax.
    - `--allow-multiple-documents` - allow yaml files which use the
      [multi-document syntax](http://www.yaml.org/spec/1.2/spec.html#YAML)
    - `--unsafe` - Instead of loading the files, simply parse them for syntax.
      A syntax-only check enables extensions and unsafe constructs which would
      otherwise be forbidden.  Using this option removes all guarantees of
      portability to other yaml implementations.
      Implies `--allow-multiple-documents`.
- `debug-statements` - Check for debugger imports and py37+ `breakpoint()`
  calls in python source.
- `detect-aws-credentials` - Checks for the existence of AWS secrets that you
  have set up with the AWS CLI.
  The following arguments are available:
  - `--credentials-file CREDENTIALS_FILE` - additional AWS CLI style
    configuration file in a non-standard location to fetch configured
    credentials from. Can be repeated multiple times.
  - `--allow-missing-credentials` - Allow hook to pass when no credentials are
    detected.
- `detect-private-key` - Checks for the existence of private keys.
- `double-quote-string-fixer` - This hook replaces double quoted strings
  with single quoted strings.
- `end-of-file-fixer` - Makes sure files end in a newline and only a newline.
- `fix-encoding-pragma` - Add `# -*- coding: utf-8 -*-` to the top of python files.
    - To remove the coding pragma pass `--remove` (useful in a python3-only codebase)
- `file-contents-sorter` - Sort the lines in specified files (defaults to alphabetical). You must provide list of target files as input to it. Note that this hook WILL remove blank lines and does NOT respect any comments.
- `flake8` - Run flake8 on your python files.
- `forbid-new-submodules` - Prevent addition of new git submodules.
- `mixed-line-ending` - Replaces or checks mixed line ending.
    - `--fix={auto,crlf,lf,no}`
        - `auto` - Replaces automatically the most frequent line ending. This is the default argument.
        - `crlf`, `lf` - Forces to replace line ending by respectively CRLF and LF.
        - `no` - Checks if there is any mixed line ending without modifying any file.
- `name-tests-test` - Assert that files in tests/ end in `_test.py`.
    - Use `args: ['--django']` to match `test*.py` instead.
- `no-commit-to-branch` - Protect specific branches from direct checkins.
    - Use `args: [--branch, staging, --branch, master]` to set the branch.
      `master` is the default if no branch argument is set.
    - `-b` / `--branch` may be specified multiple times to protect multiple
      branches.
    - `-p` / `--pattern` can be used to protect branches that match a supplied regex
      (e.g. `--pattern, release/.*`). May be specified multiple times.
- `pretty-format-json` - Checks that all your JSON files are pretty.  "Pretty"
  here means that keys are sorted and indented.  You can configure this with
  the following commandline options:
    - `--autofix` - automatically format json files
    - `--indent ...` - Control the indentation (either a number for a number of spaces or a string of whitespace).  Defaults to 4 spaces.
    - `--no-sort-keys` - when autofixing, retain the original key ordering (instead of sorting the keys)
    - `--top-keys comma,separated,keys` - Keys to keep at the top of mappings.
- `requirements-txt-fixer` - Sorts entries in requirements.txt and removes incorrect entry for `pkg-resources==0.0.0`
- `sort-simple-yaml` - Sorts simple YAML files which consist only of top-level
  keys, preserving comments and blocks.

  Note that `sort-simple-yaml` by default matches no `files` as it enforces a
  very specific format.  You must opt in to this by setting `files`, for
  example:

  ```yaml
      -   id: sort-simple-yaml
          files: ^config/simple/
  ```

- `trailing-whitespace` - Trims trailing whitespace.
    - To preserve Markdown [hard linebreaks](https://github.github.com/gfm/#hard-line-break)
      use `args: [--markdown-linebreak-ext=md]` (or other extensions used
      by your markdownfiles).  If for some reason you want to treat all files
      as markdown, use `--markdown-linebreak-ext=*`.
    - By default, this hook trims all whitespace from the ends of lines.
      To specify a custom set of characters to trim instead, use `args: [--chars,"<chars to trim>"]`.

### Deprecated / replaced hooks

- `autopep8-wrapper`: instead use
  [mirrors-autopep8](https://github.com/pre-commit/mirrors-autopep8)
- `pyflakes`: instead use `flake8`

### As a standalone package

If you'd like to use these hooks, they're also available as a standalone
package.

Simply `pip install pre-commit-hooks`
