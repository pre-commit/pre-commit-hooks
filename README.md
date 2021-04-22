[![build status](https://github.com/pre-commit/pre-commit-hooks/actions/workflows/main.yml/badge.svg)](https://github.com/pre-commit/pre-commit-hooks/actions/workflows/main.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pre-commit/pre-commit-hooks/main.svg)](https://results.pre-commit.ci/latest/github/pre-commit/pre-commit-hooks/main)

pre-commit-hooks
================

Some out-of-the-box hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit


### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0  # Use the ref you want to point at
    hooks:
    -   id: trailing-whitespace
    # -   id: ...
```

### Hooks available

#### `check-added-large-files`
Prevent giant files from being committed.
  - Specify what is "too large" with `args: ['--maxkb=123']` (default=500kB).
  - Limits checked files to those indicated as staged for addition by git.
  - If `git-lfs` is installed, lfs files will be skipped
    (requires `git-lfs>=2.2.1`)
  - `--enforce-all` - Check all listed files not just those staged for
    addition.

#### `check-ast`
Simply check whether files parse as valid python.

#### `check-builtin-literals`
Require literal syntax when initializing empty or zero Python builtin types.
  - Allows calling constructors with positional arguments (e.g., `list('abc')`).
  - Allows calling constructors from the `builtins` (`__builtin__`) namespace (`builtins.list()`).
  - Ignore this requirement for specific builtin types with `--ignore=type1,type2,…`.
  - Forbid `dict` keyword syntax with `--no-allow-dict-kwargs`.

#### `check-case-conflict`
Check for files with names that would conflict on a case-insensitive filesystem like MacOS HFS+ or Windows FAT.

#### `check-docstring-first`
Checks for a common error of placing code before the docstring.

#### `check-executables-have-shebangs`
Checks that non-binary executables have a proper shebang.

#### `check-illegal-windows-names`
Check for files that cannot be created on Windows.

#### `check-json`
Attempts to load all json files to verify syntax.

#### `check-merge-conflict`
Check for files that contain merge conflict strings.
  - `--assume-in-merge` - Allows running the hook when there is no ongoing merge operation

#### `check-shebang-scripts-are-executable`
Checks that scripts with shebangs are executable.

#### `check-symlinks`
Checks for symlinks which do not point to anything.

#### `check-toml`
Attempts to load all TOML files to verify syntax.

#### `check-vcs-permalinks`
Ensures that links to vcs websites are permalinks.
  - `--additional-github-domain DOMAIN` - Add check for specified domain.
    Can be repeated multiple times.  for example, if your company uses
    GitHub Enterprise you may use something like
    `--additional-github-domain github.example.com`

#### `check-xml`
Attempts to load all xml files to verify syntax.

#### `check-yaml`
Attempts to load all yaml files to verify syntax.
  - `--allow-multiple-documents` - allow yaml files which use the
    [multi-document syntax](http://www.yaml.org/spec/1.2/spec.html#YAML)
  - `--unsafe` - Instead of loading the files, simply parse them for syntax.
    A syntax-only check enables extensions and unsafe constructs which would
    otherwise be forbidden.  Using this option removes all guarantees of
    portability to other yaml implementations.
    Implies `--allow-multiple-documents`.

#### `debug-statements`
Check for debugger imports and py37+ `breakpoint()` calls in python source.

#### `destroyed-symlinks`
Detects symlinks which are changed to regular files with a content of a path
which that symlink was pointing to.
This usually happens on Windows when a user clones a repository that has
symlinks but they do not have the permission to create symlinks.

#### `detect-aws-credentials`
Checks for the existence of AWS secrets that you have set up with the AWS CLI.
The following arguments are available:
- `--credentials-file CREDENTIALS_FILE` - additional AWS CLI style
  configuration file in a non-standard location to fetch configured
  credentials from. Can be repeated multiple times.
- `--allow-missing-credentials` - Allow hook to pass when no credentials are detected.

#### `detect-private-key`
Checks for the existence of private keys.

#### `double-quote-string-fixer`
This hook replaces double quoted strings with single quoted strings.

#### `end-of-file-fixer`
Makes sure files end in a newline and only a newline.

#### `file-contents-sorter`
Sort the lines in specified files (defaults to alphabetical).
You must provide the target [`files`](https://pre-commit.com/#config-files) as input.
Note that this hook WILL remove blank lines and does NOT respect any comments.
All newlines will be converted to line feeds (`\n`).

The following arguments are available:
- `--ignore-case` - fold lower case to upper case characters.
- `--unique` - ensure each line is unique.

#### `fix-byte-order-marker`
removes UTF-8 byte order marker

#### `fix-encoding-pragma`

_Deprecated since py2 is EOL - use [pyupgrade](https://github.com/asottile/pyupgrade) instead._

Add `# -*- coding: utf-8 -*-` to the top of python files.
  - To remove the coding pragma pass `--remove` (useful in a python3-only codebase)

#### `forbid-new-submodules`
Prevent addition of new git submodules.

This is intended as a helper to migrate away from submodules.  If you want to
ban them entirely use `forbid-submodules`

#### `forbid-submodules`
forbids any submodules in the repository.

#### `mixed-line-ending`
Replaces or checks mixed line ending.
  - `--fix={auto,crlf,lf,no}`
      - `auto` - Replaces automatically the most frequent line ending. This is the default argument.
      - `crlf`, `lf` - Forces to replace line ending by respectively CRLF and LF.
          - This option isn't compatible with git setup check-in LF check-out CRLF as git smudge this later than the hook is invoked.
      - `no` - Checks if there is any mixed line ending without modifying any file.

#### `name-tests-test`
verifies that test files are named correctly.
- `--pytest` (the default): ensure tests match `.*_test\.py`
- `--pytest-test-first`: ensure tests match `test_.*\.py`
- `--django` / `--unittest`: ensure tests match `test.*\.py`

#### `no-commit-to-branch`
Protect specific branches from direct checkins.
  - Use `args: [--branch, staging, --branch, main]` to set the branch.
    Both `main` and `master` are protected by default if no branch argument is set.
  - `-b` / `--branch` may be specified multiple times to protect multiple
    branches.
  - `-p` / `--pattern` can be used to protect branches that match a supplied regex
    (e.g. `--pattern, release/.*`). May be specified multiple times.

Note that `no-commit-to-branch` is configured by default to [`always_run`](https://pre-commit.com/#config-always_run).
As a result, it will ignore any setting of [`files`](https://pre-commit.com/#config-files),
[`exclude`](https://pre-commit.com/#config-exclude), [`types`](https://pre-commit.com/#config-types)
or [`exclude_types`](https://pre-commit.com/#config-exclude_types).
Set [`always_run: false`](https://pre-commit.com/#config-always_run) to allow this hook to be skipped according to these
file filters. Caveat: In this configuration, empty commits (`git commit --allow-empty`) would always be allowed by this hook.

#### `pretty-format-json`
Checks that all your JSON files are pretty.  "Pretty"
here means that keys are sorted and indented.  You can configure this with
the following commandline options:
  - `--autofix` - automatically format json files
  - `--indent ...` - Control the indentation (either a number for a number of spaces or a string of whitespace).  Defaults to 2 spaces.
  - `--no-ensure-ascii` preserve unicode characters instead of converting to escape sequences
  - `--no-sort-keys` - when autofixing, retain the original key ordering (instead of sorting the keys)
  - `--top-keys comma,separated,keys` - Keys to keep at the top of mappings.

#### `requirements-txt-fixer`
Sorts entries in requirements.txt and constraints.txt and removes incorrect entry for `pkg-resources==0.0.0`

#### `sort-simple-yaml`
Sorts simple YAML files which consist only of top-level
keys, preserving comments and blocks.

Note that `sort-simple-yaml` by default matches no `files` as it enforces a
very specific format.  You must opt in to this by setting [`files`](https://pre-commit.com/#config-files), for example:

```yaml
    -   id: sort-simple-yaml
        files: ^config/simple/
```


#### `trailing-whitespace`
Trims trailing whitespace.
  - To preserve Markdown [hard linebreaks](https://github.github.com/gfm/#hard-line-break)
    use `args: [--markdown-linebreak-ext=md]` (or other extensions used
    by your markdownfiles).  If for some reason you want to treat all files
    as markdown, use `--markdown-linebreak-ext=*`.
  - By default, this hook trims all whitespace from the ends of lines.
    To specify a custom set of characters to trim instead, use `args: [--chars,"<chars to trim>"]`.

### Deprecated / replaced hooks

- `check-byte-order-marker`: instead use fix-byte-order-marker

### As a standalone package

If you'd like to use these hooks, they're also available as a standalone package.

Simply `pip install pre-commit-hooks`
