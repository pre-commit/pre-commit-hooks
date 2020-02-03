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

- <a name="check-added-large-files">`check-added-large-files`</a> - Prevent giant files from being committed.
    - Specify what is "too large" with `args: ['--maxkb=123']` (default=500kB).
    - If `git-lfs` is installed, lfs files will be skipped
      (requires `git-lfs>=2.2.1`)
- <a name="check-ast">`check-ast`</a> - Simply check whether files parse as valid python.
- <a name="check-builtin-literals">`check-builtin-literals`</a> - Require literal syntax when initializing empty or zero Python builtin types.
    - Allows calling constructors with positional arguments (e.g., `list('abc')`).
    - Allows calling constructors from the `builtins` (`__builtin__`) namespace (`builtins.list()`).
    - Ignore this requirement for specific builtin types with `--ignore=type1,type2,…`.
    - Forbid `dict` keyword syntax with `--no-allow-dict-kwargs`.
- <a name="check-byte-order-marker">`check-byte-order-marker`</a> - Forbid files which have a UTF-8 byte-order marker
- <a name="check-case-conflict">`check-case-conflict`</a> - Check for files with names that would conflict on a
  case-insensitive filesystem like MacOS HFS+ or Windows FAT.
- <a name="check-docstring-first">`check-docstring-first`</a> - Checks for a common error of placing code before
  the docstring.
- <a name="check-executables-have-shebangs">`check-executables-have-shebangs`</a> - Checks that non-binary executables have a
  proper shebang.
- <a name="check-json">`check-json`</a> - Attempts to load all json files to verify syntax.
- <a name="check-merge-conflict">`check-merge-conflict`</a> - Check for files that contain merge conflict strings.
- <a name="check-symlinks">`check-symlinks`</a> - Checks for symlinks which do not point to anything.
- <a name="check-toml">`check-toml`</a> - Attempts to load all TOML files to verify syntax.
- <a name="check-vcs-permalinks">`check-vcs-permalinks`</a> - Ensures that links to vcs websites are permalinks.
- <a name="check-xml">`check-xml`</a> - Attempts to load all xml files to verify syntax.
- <a name="check-yaml">`check-yaml`</a> - Attempts to load all yaml files to verify syntax.
    - `--allow-multiple-documents` - allow yaml files which use the
      [multi-document syntax](http://www.yaml.org/spec/1.2/spec.html#YAML)
    - `--unsafe` - Instead of loading the files, simply parse them for syntax.
      A syntax-only check enables extensions and unsafe constructs which would
      otherwise be forbidden.  Using this option removes all guarantees of
      portability to other yaml implementations.
      Implies `--allow-multiple-documents`.
- <a name="debug-statements">`debug-statements`</a> - Check for debugger imports and py37+ `breakpoint()`
  calls in python source.
- <a name="detect-aws-credentials">`detect-aws-credentials`</a> - Checks for the existence of AWS secrets that you
  have set up with the AWS CLI.
  The following arguments are available:
  - `--credentials-file CREDENTIALS_FILE` - additional AWS CLI style
    configuration file in a non-standard location to fetch configured
    credentials from. Can be repeated multiple times.
  - `--allow-missing-credentials` - Allow hook to pass when no credentials are
    detected.
- <a name="detect-private-key">`detect-private-key`</a> - Checks for the existence of private keys.
- <a name="double-quote-string-fixer">`double-quote-string-fixer`</a> - This hook replaces double quoted strings
  with single quoted strings.
- <a name="end-of-file-fixer">`end-of-file-fixer`</a> - Makes sure files end in a newline and only a newline.
- <a name="fix-encoding-pragma">`fix-encoding-pragma`</a> - Add `# -*- coding: utf-8 -*-` to the top of python files.
    - To remove the coding pragma pass `--remove` (useful in a python3-only codebase)
- <a name="file-contents-sorter">`file-contents-sorter`</a> - Sort the lines in specified files (defaults to alphabetical). You must provide list of target files as input to it. Note that this hook WILL remove blank lines and does NOT respect any comments.
- <a name="flake8">`flake8`</a> - Run flake8 on your python files.
- <a name="forbid-new-submodules">`forbid-new-submodules`</a> - Prevent addition of new git submodules.
- <a name="mixed-line-ending">`mixed-line-ending`</a> - Replaces or checks mixed line ending.
    - `--fix={auto,crlf,lf,no}`
        - `auto` - Replaces automatically the most frequent line ending. This is the default argument.
        - `crlf`, `lf` - Forces to replace line ending by respectively CRLF and LF.
            - This option isn't compatible with git setup check-in LF check-out CRLF as git smudge this later than the hook is invoked.
        - `no` - Checks if there is any mixed line ending without modifying any file.
- <a name="name-tests-test">`name-tests-test`</a> - Assert that files in tests/ end in `_test.py`.
    - Use `args: ['--django']` to match `test*.py` instead.
- <a name="no-commit-to-branch">`no-commit-to-branch`</a> - Protect specific branches from direct checkins.
    - Use `args: [--branch, staging, --branch, master]` to set the branch.
      `master` is the default if no branch argument is set.
    - `-b` / `--branch` may be specified multiple times to protect multiple
      branches.
    - `-p` / `--pattern` can be used to protect branches that match a supplied regex
      (e.g. `--pattern, release/.*`). May be specified multiple times.
- <a name="pretty-format-json">`pretty-format-json`</a> - Checks that all your JSON files are pretty.  "Pretty"
  here means that keys are sorted and indented.  You can configure this with
  the following commandline options:
    - `--autofix` - automatically format json files
    - `--indent ...` - Control the indentation (either a number for a number of spaces or a string of whitespace).  Defaults to 4 spaces.
    - `--no-ensure-ascii` preserve unicode characters instead of converting to escape sequences
    - `--no-sort-keys` - when autofixing, retain the original key ordering (instead of sorting the keys)
    - `--top-keys comma,separated,keys` - Keys to keep at the top of mappings.
- <a name="requirements-txt-fixer">`requirements-txt-fixer`</a> - Sorts entries in requirements.txt and removes incorrect entry for `pkg-resources==0.0.0`
- <a name="sort-simple-yaml">`sort-simple-yaml`</a> - Sorts simple YAML files which consist only of top-level
  keys, preserving comments and blocks.

  Note that `sort-simple-yaml` by default matches no `files` as it enforces a
  very specific format.  You must opt in to this by setting `files`, for
  example:

  ```yaml
      -   id: sort-simple-yaml
          files: ^config/simple/
  ```

- <a name="trailing-whitespace">`trailing-whitespace`</a> - Trims trailing whitespace.
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
