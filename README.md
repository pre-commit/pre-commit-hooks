[![Build Status](https://asottile.visualstudio.com/asottile/_apis/build/status/pre-commit.pre-commit-hooks?branchName=master)](https://asottile.visualstudio.com/asottile/_build/latest?definitionId=17&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/17/master.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=17&branchName=master)

pre-commit-hooks
================

Some out-of-the-box hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit


### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

    -   repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v2.2.3  # Use the ref you want to point at
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
- `sort-simple-yaml` - Sorts simple YAML files which consist only of top-level keys, preserving comments and blocks.
- `trailing-whitespace` - Trims trailing whitespace.
    - To preserve Markdown [hard linebreaks](https://github.github.com/gfm/#hard-line-break)
      use `args: [--markdown-linebreak-ext=md]` (or other extensions used
      by your markdownfiles).  If for some reason you want to treat all files
      as markdown, use `--markdown-linebreak-ext=*`.
- `check-xml-encoding` - Checks that xml files have required encoding as first line.
    - To specify desired encoding use `args: [--encoding]`. Example:
    `args: [
            --encoding, '<?xml version="1.0" encoding="utf-8"?>',
          ]`
- `check-location` - Checks that specified files are located inside specified directories.
    - To specify desired encoding use: `args: [--directories, --files]`. Example:
    `args: [
          --directories, '^[^\/]+$',
          --directories, '.*\/controllers$',
          --directories, '.*\/data$',
          --directories, '.*\/i18n$',
          --directories, '.*\/models$',
          --directories, '.*\/report$',
          --directories, '.*\/security$',
          --directories, '.*\/static\/img$',
          --directories, '.*\/static\/lib\/external_lib$',
          --directories, '.*\/static\/src\/js$',
          --directories, '.*\/static\/src\/css$',
          --directories, '.*\/static\/src\/less$',
          --directories, '.*\/static\/src\/xml$',
          --directories, '.*\/static\/tests$',
          --directories, '.*[^\/static]\/tests$',
          --directories, '.*\/views$',
          --directories, '.*\/wizard$',
          --files, '__init__.py$ __openerp__.py$',
          --files, '__init__.py$ .*\.py$ main.py$',
          --files, '.*_data\.xml$ .*_demo\.xml$',
          --files, '.*\.po$',
          --files, '__init__.py$ .*\.py$',
          --files, '__init__.py$ .*\.py$ .*_views\.xml$ .*_reports\.xml$ .*_templates\.xml$',
          --files, 'ir.model.access.csv$ .*_security\.xml$',
          --files, '.*\.png$ .*\.jpg$',
          --files, '.*\$',
          --files, '.*\.js$',
          --files, '.*\.css$',
          --files, '.*\.less$',
          --files, '.*\.xml$',
          --files, '.*\.tour\.js$',
          --files, '__init__.py$ test_.*\.py',
          --files, '.*_templates\.xml$ .*_views\.xml$',
          --files, '.*\.py$ .*_views\.xml$',
        ]`
    
    Both arguments receive a regular expression.
    
    Number of specified directories must match number of specified files.
    
    Order matters: First 'files' types found will be checked to be inside of first 'directories'.
- `check-using-pylint` - Check Python Using Pylint.
    - To exclude files from the check, use `args: [--exclude]`. Example:
    `args: [
            --exclude, '.*(\/)*__openerp__.py$',
          ]`
    
    Receives a regular expression
- `check-branch-name` - Checks current branch name.
    - To specify correct branch name use `args: [--regex]`. Example:
    `args: [
          --regex, 'develop\..+?\.(DEFECTO|INVES|MEJORA)\.\d+(_\d+)*'
        ]`
- `check-line` - Checks desired lines are formatted as desired in python and xml files.
    - To specify correct branch name use `args: [--line-to-check, --regexp-to-match]`. Example:
    `args: [
          --line-to-check, '^(\t| )*<field.+',
          --line-to-check, '^(\t| )*<record.+',
          --line-to-check, '.+fields.Many2one.+',
          --line-to-check, '.+fields.One2many.+',
          --line-to-check, '.+fields.Many2many.+',
          --line-to-check, 'class.+',
          --regexp-to-match, '^(\t| )*<field name=".+"',
          --regexp-to-match, '^(\t| )*<record id=".+"',
          --regexp-to-match, '^(\t| )*.+_id = fields.Many2one\(',
          --regexp-to-match, '^(\t| )*.+_ids = fields.One2many\(',
          --regexp-to-match, '^(\t| )*.+_ids = fields.Many2many\(',
          --regexp-to-match, 'class ([A-Z]+[a-z0-9]+)+\(.+\):',
        ]`
- `check-model-name` - Checks that odoo model name uses dot notation and has module name as prefix.
- `check-class-docstring` - Checks that each python class has a docstring.
- `check-view-name` - Checks that odoo views name follow odoo guidelines.
- `check-view-fields-order` - Checks view fields order follow odoo guidelines.

### Deprecated / replaced hooks

- `autopep8-wrapper`: instead use
  [mirrors-autopep8](https://github.com/pre-commit/mirrors-autopep8)
- `pyflakes`: instead use `flake8`

### As a standalone package

If you'd like to use these hooks, they're also available as a standalone
package.

Simply `pip install pre-commit-hooks`
