4.5.0 - 2023-10-07
==================

### Features
- `requirements-txt-fixer`: also sort `constraints.txt` by default.
    - #857 PR by @lev-blit.
    - #830 issue by @PLPeeters.
- `debug-statements`: add `bpdb` debugger.
    - #942 PR by @mwip.
    - #941 issue by @mwip.

### Fixes
- `file-contents-sorter`: fix sorting an empty file.
    - #944 PR by @RoelAdriaans.
    - #935 issue by @paduszyk.
- `double-quote-string-fixer`: don't rewrite inside f-strings in 3.12+.
    - #973 PR by @asottile.
    - #971 issue by @XuehaiPan.

## Migrating
- now requires python >= 3.8.
    - #926 PR by @asottile.
    - #927 PR by @asottile.

4.4.0 - 2022-11-23
==================

### Features
- `forbid-submodules`: new hook which outright bans submodules.
    - #815 PR by @asottile.
    - #707 issue by @ChiefGokhlayeh.

4.3.0 - 2022-06-07
==================

### Features
- `check-executables-have-shebangs`: use `git config core.fileMode` to
  determine if it should query `git`.
    - #730 PR by @Kurt-von-Laven.
- `name-tests-test`: add `--pytest-test-first` test convention.
    - #779 PR by @asottile.

### Fixes
- `check-shebang-scripts-are-executable`: update windows instructions.
    - #774 PR by @mdeweerd.
    - #770 issue by @mdeweerd.
- `check-toml`: use stdlib `tomllib` when available.
    - #771 PR by @DanielNoord.
    - #755 issue by @sognetic.
- `check-added-large-files`: don't run on non-file `stages`.
    - #778 PR by @asottile.
    - #777 issue by @skyj.

4.2.0 - 2022-04-06
==================

### Features
- `name-tests-test`: updated display text.
    - #713 PR by @asottile.
- `check-docstring-first`: make output more parsable.
    - #748 PR by @asottile.
- `check-merge-conflict`: make output more parsable.
    - #748 PR by @asottile.
- `debug-statements`: make output more parsable.
    - #748 PR by @asottile.

### Fixes
- `check-merge-conflict`: fix detection of `======` conflict marker on windows.
    - #748 PR by @asottile.

### Updating
- Drop python<3.7.
    - #719 PR by @asottile.
- Changed default branch from `master` to `main`.
    - #744 PR by @asottile.

4.1.0 - 2021-12-22
==================

### Features
- `debug-statements`: add `pdbr` debugger.
    - #614 PR by @cansarigol.
- `detect-private-key`: add detection for additional key types.
    - #658 PR by @ljmf00.
- `check-executables-have-shebangs`: improve messaging on windows.
    - #689 PR by @pujitm.
    - #686 issue by @jmerdich.
- `check-added-large-files`: support `--enforce-all` with `git-lfs`.
    - #674 PR by @amartani.
    - #560 issue by @jeremy-coulon.

### Fixes
- `check-case-conflict`: improve performance.
    - #626 PR by @guykisel.
    - #625 issue by @guykisel.
- `forbid-new-submodules`: fix false-negatives for `pre-push`.
    - #619 PR by @m-khvoinitsky.
    - #609 issue by @m-khvoinitsky.
- `check-merge-conflict`: fix execution in git worktrees.
    - #662 PR by @errsyn.
    - #638 issue by @daschuer.

### Misc.
- Normalize case of hook names and descriptions.
    - #671 PR by @dennisroche.
    - #673 PR by @revolter.

4.0.1 - 2021-05-16
==================

### Fixes
- `check-shebang-scripts-are-executable` fix entry point.
    - #602 issue by @Person-93.
    - #603 PR by @scop.

4.0.0 - 2021-05-14
==================

### Features
- `check-json`: report duplicate keys.
    - #558 PR by @AdityaKhursale.
    - #554 issue by @adamchainz.
- `no-commit-to-branch`: add `main` to default blocked branches.
    - #565 PR by @ndevenish.
- `check-case-conflict`: check conflicts in directory names as well.
    - #575 PR by @slsyy.
    - #70 issue by @andyjack.
- `check-vcs-permalinks`: forbid other branch names.
    - #582 PR by @jack1142.
    - #581 issue by @jack1142.
- `check-shebang-scripts-are-executable`: new hook which ensures shebang'd
  scripts are executable.
    - #545 PR by @scop.

### Fixes
- `check-executables-have-shebangs`: Short circuit shebang lookup on windows.
    - #544 PR by @scop.
- `requirements-txt-fixer`: Fix comments which have indentation
    - #549 PR by @greshilov.
    - #548 issue by @greshilov.
- `pretty-format-json`: write to stdout using UTF-8 encoding.
    - #571 PR by @jack1142.
    - #570 issue by @jack1142.
- Use more inclusive language.
    - #599 PR by @asottile.

### Breaking changes
- Remove deprecated hooks: `flake8`, `pyflakes`, `autopep8-wrapper`.
    - #597 PR by @asottile.


3.4.0 - 2020-12-15
==================

### Features
- `file-contents-sorter`: Add `--unique` argument
    - #524 PR by @danielhoherd.
- `check-vcs-permalinks`: Add `--additional-github-domain` option
    - #530 PR by @youngminz.
- New hook: `destroyed-symlinks` to detect unintentional symlink-breakages on
  windows.
    - #511 PR by @m-khvoinitsky.

3.3.0 - 2020-10-20
==================

### Features
- `file-contents-sorter`: add `--ignore-case` option for case-insensitive
  sorting
    - #514 PR by @Julian.
- `check-added-large-files`: add `--enforce-all` option to check non-added
  files as well
    - #519 PR by @mshawcroft.
    - #518 issue by @mshawcroft.
- `fix-byte-order-marker`: new hook which fixes UTF-8 byte-order marker.
    - #522 PR by @jgowdy.

### Deprecations
- `check-byte-order-marker` is now deprecated for `fix-byte-order-marker`

3.2.0 - 2020-07-30
==================

### Features
- `debug-statements`: add support for `pydevd_pycharm` debugger
    - #502 PR by @jgeerds.

### Fixes
- `check-executables-have-shebangs`: fix git-quoted files on windows (spaces,
  non-ascii, etc.)
    - #509 PR by @pawamoy.
    - #508 issue by @pawamoy.

3.1.0 - 2020-05-20
==================

### Features
- `check-executables-have-shebangs`: on windows, validate the mode bits using
  `git`
    - #480 PR by @mxr.
    - #435 issue by @dstandish.
- `requirements-txt-fixer`: support more operators
    - #483 PR by @mxr.
    - #331 issue by @hackedd.

### Fixes
- `pre-commit-hooks-removed`: Fix when removed hooks used `args`
    - #487 PR by @pedrocalleja.
    - #485 issue by @pedrocalleja.

3.0.1 - 2020-05-16
==================

### Fixes
- `check-toml`: use UTF-8 encoding to load toml files
    - #479 PR by @mxr.
    - #474 issue by @staticdev.

3.0.0 - 2020-05-14
==================

### Features
- `detect-aws-credentials`: skip empty aws keys
    - #450 PR by @begoon.
    - #449 issue by @begoon.
- `debug-statements`: add detection `wdb` debugger
    - #452 PR by @itsdkey.
    - #451 issue by @itsdkey.
- `requirements-txt-fixer`: support line continuation for dependencies
    - #469 PR by @aniketbhatnagar.
    - #465 issue by @aniketbhatnagar.

### Fixes
- `detect-aws-credentials`: fix `UnicodeDecodeError` when running on non-UTF8
  files.
    - #453 PR by @asottile.
    - #393 PR by @a7p
    - #346 issue by @rpdelaney.

### Updating
- pre-commit/pre-commit-hooks now requires python3.6.1+
    - #447 PR by @asottile.
    - #455 PR by @asottile.
- `flake8` / `pyflakes` have been removed, use `flake8` from `pycqa/flake8`
  instead:

  ```yaml
  -   repo: https://gitlab.com/pycqa/flake8
      rev: 3.8.1
      hooks:
      -   id: flake8
  ```

    - #476 PR by @asottile.
    - #477 PR by @asottile.
    - #344 issue by @asottile.


2.5.0 - 2020-02-04
==================

### Fixes
- Fix sorting of requirements which use `egg=...`
    - #425 PR by @vinayinvicible.
- Fix over-eager regular expression for test filename matching
    - #429 PR by @rrauenza.

### Updating
- Use `flake8` from `pycqa/flake8` instead:

  ```yaml
  -   repo: https://gitlab.com/pycqa/flake8
      rev: 3.7.9
      hooks:
      -   id: flake8
  ```

2.4.0 - 2019-10-28
==================

### Features
- Add diff output to `pretty-format-json` when run without `--autofix`.
    - #408 PR by @joepin.
- Add `--chars` option to `trailing-whitespace` fixer to control which
  characters are stripped instead of all whitespace.
    - #421 PR by @iconmaster5326.

### Fixes
- Fix `requirements-txt-fixer` when file does not end in a newline.
    - #414 issue by @barakreif.
    - #415 PR by @barakreif.
- Fix double printing of filename in `pretty-format-json`.
    - #419 PR by @asottile.

2.3.0 - 2019-08-05
==================

### Features
- Add `rpdb` to detected debuggers in `debug-statements`
    - #389 PR by @danlamanna.
- Add `check-toml` hook
    - #400 PR by @MarSoft.
    - #400 PR by @ssbarnea.

### Fixes
- Add `__main__` block to `pre_commit.file_contents_sorter` so it can be
  invoked using `python -m`
    - #405 PR by @squeaky-pl.

### Misc.
- Fix `git-lfs` tests in azure pipelines
    - #403 PR by @ssbarnea.

2.2.3 - 2019-05-16
==================

### Fixes
- Handle CRLF line endings in `double-quote-string-fixer`
    - #385 issue by @Trim21.
    - #386 PR by @asottile.

2.2.2 - 2019-05-15
==================

### Fixes
- Handle CRLF line endings in `fix-encoding-pragma`
    - #384 PR by @asottile.

2.2.1 - 2019-04-21
==================

### Fixes
- Use UTF-8 to load yaml files
    - #377 issue by @roottool.
    - #378 PR by @roottool.

2.2.0 - 2019-04-20
==================

### Features
- Switch from `pyyaml` to `ruamel.yaml`
    - This enforces (among other things) duplicate key checking in yaml.
    - #351 PR by @asottile.
- Add a new `--pattern` option to `no-commit-to-branch` for regex matching
  branch names.
    - #375 issue by @marcjay.
    - #376 PR by @marcjay.

### Fixes
- Set `require_serial: true` for flake8
    - flake8 internally uses multiprocessing.
    - #358 PR by @asottile.
- Don't run `check-executables-have-shebangs` / `trailing-whitespace` hooks
  during the `commit-msg` stage.
    - #361 issue by @revolter.
    - #362 PR by @revolter.
- Run `check-byte-order-marker` against `types: [text]`
    - #371 PR by @tobywf.
    - #372 PR by @tobywf.
- Do not require UTF-8-encoded files for `check-docstring-first`
    - #345 issue by @x007007007.
    - #374 PR by @asottile.

### Misc.
- `pre-commit-hooks` now is type checked with mypy.
    - #360 PR by @asottile.

2.1.0 - 2018-12-26
==================

### Features
- Detect PGP/GPG private keys in `detect-private-key`
    - #329 PR by @rpdelaney.
- Report filenames when fixing files in `mixed-line-endings`
    - #341 PR by @gimbo.
    - #340 issuey by @gimbo.

### Fixes
- Handle CRLF / CR line endings in `end-of-file-fixer`
    - #327 PR by @mtkennerly.

### Docs

- Clarify and document arguments for `detect-aws-credentials`
    - #333 PR by @rpdelaney.
- Clarify `autopep8-wrapper` is deprecated in description
    - #343 PR by @TheKevJames.


2.0.0 - 2018-10-12
==================

### Breaking changes

- `autopep8-wrapper` has been moved to
  [pre-commit/mirrors-autopep8][mirrors-autopep8]
    - #92 issue by @asottile.
    - #319 issue by @blaggacao.
    - #321 PR by @asottile.
- `trailing-whitespace` defaults to `--no-markdown-linebreak-ext`
    - #310 issue by @asottile.
    - #324 PR by @asottile.
- `hooks.yaml` (legacy pre-commit hook metadata) deleted
    - #323 PR by @asottile.
- pre-`types` compatibility metadata removed
    - #323 PR @asottile.

### Docs

- Correct documentation for `no-commit-to-branch`
    - #318 PR by @milin.

### Updating

- Minimum supported version of `pre-commit` is now 0.15.0
- Use `autopep8` from [pre-commit/mirrors-autopep8][mirrors-autopep8]
- To keep mardown hard linebreaks, for `trailing-whitespace` use
  `args: [--markdown-linebreak-ext=md,markdown]` (the previous default value)

[mirrors-autopep8]: https://github.com/pre-commit/mirrors-autopep8

1.4.0-1 - 2018-09-27
====================

(Note: this is a tag-only release as no code changes occurred)

### Fixes
- Don't run `end-of-file-fixer` during `commit-msg` stage
    - #315 issue by @revolter.
    - #317 PR by @revolter.

1.4.0 - 2018-07-22
==================

### Features
- `no-commit-to-branch`: allow `--branch` to be specified multiple times
    - #190 PR by @moas.
    - #294 PR by @asottile.
- `check-merge-conflict`: add `--assume-in-merge` to force checks outside of a
  merge commit situation
    - #300 issue by @vinayinvicible.
    - #301 PR by @vinayinvicible.

### Fixes
- Don't match whitespace in VCS urls
    - #293 PR by @asottile.
- Fix invalid escape sequences
    - #296 PR by @asottile.
- Fix `ResourcesWarning`s
    - #297 PR by @asottile.

### Misc
- Test against python3.7
    - #304 PR by @expobrain.

1.3.0 - 2018-05-28
==================

### Features
- Add an `--unsafe` argument to `check-yaml` to allow custom yaml tags
    - #273 issue by @blackillzone.
    - #274 PR by @asottile.
- Automatically remove `pkg-resources==0.0.0` in `requirements-txt-fixer`
    - #275 PR by @nvtkaszpir.
- Detect `breakpoint()` (python3.7+) in `debug-statements` hook.
    - #283 PR by @asottile.
- Detect sshcom and putty hooks in `detect-private-key`
    - #287 PR by @vin01.

### Fixes
- Open files as UTF-8 (`autopep8-wrapper`, `check-docstring-first`,
  `double-quote-string-fixer`)
    - #279 PR by @nvtkaszpir.
- Fix `AttributeError` in `check-builtin-literals` for some functions
    - #285 issue by @EgoWumpus.
    - #286 PR by @asottile.

1.2.3 - 2018-02-28
==================

### Fixes
- `trailing-whitespace` entrypoint was incorrect.
    - f6780b9 by @asottile.

1.2.2 - 2018-02-28
==================

### Fixes
- `trailing-whitespace` no longer adds a missing newline at end-of-file
    - #270 issue by @fractos.
    - #271 PR by @asottile.

1.2.1-1 - 2018-02-24
====================

(Note: this is a tag-only release as no code changes occurred)

### Fixes:
- Don't pass filenames for `no-commit-to-branch`
    - #268 issue by @dongyuzheng.
    - #269 PR by @asottile.

1.2.1 - 2018-02-19
==================
### Fixes:
- `detect-aws-credentials` false positive when key was empty
    - #258 issue by @PVSec.
    - #260 PR by @PVSec.
- `no-commit-to-branch` no longer crashes when not on a branch
    - #265 issue by @hectorv.
    - #266 PR by @asottile.

1.2.0 - 2018-01-13
==================
### Features:
- Add new `check-builtin-literals` hook.
    - #249 #251 PR by @benwebber.
- `pretty-format-json` no longer depends on `simplejson`.
    - #254 PR by @cas--.
- `detect-private-key` now detects gcp keys.
    - #255 issue by @SaMnCo @nicain.
    - #256 PR by @nicain.

1.1.1 - 2017-10-19
==================
### Fixes:
- Fix output interleaving in `check-vcs-permalinks` under python3.
    - #245 PR by @asottile.

1.1.0 - 2017-10-12
==================
### Features:
- `check-yaml` gains a `--allow-multiple-documents` (`-m`) argument to allow
  linting of files using the
  [multi document syntax](http://www.yaml.org/spec/1.2/spec.html#YAML)
    - pre-commit/pre-commit#635 issue by @geekobi.
    - #244 PR by @asottile.

1.0.0 - 2017-10-09
==================
### Features:
- New hook: `check-vcs-permalinks` for ensuring permalinked github urls.
    - #241 PR by @asottile.

### Fixes:
- Fix `trailing-whitespace` for non-utf8 files on macos
    - #242 PR by @asottile.
- Fix `requirements-txt-fixer` for files ending in comments
    - #243 PR by @asottile.

0.9.5 - 2017-09-27
==================
- Fix mixed-line-endings `--fix=...` when whole file is a different ending

0.9.4 - 2017-09-19
==================
- Fix entry point for `mixed-line-ending`

0.9.3 - 2017-09-07
==================
- New hook: `mixed-line-ending`

0.9.2 - 2017-08-21
==================
- Report full python version in `check-ast`.
- Apply a more strict regular expression for `name-tests-test`
- Upgrade binding for `git-lfs` for `check-added-large-files`.  The oldest
  version that is supported is 2.2.1 (2.2.0 will incorrectly refer to all
  files as "lfs" (false negative) and earlier versions will crash.
- `debug-statements` now works for non-utf-8 files.

0.9.1 - 2017-07-02
==================
- Add `check-executables-have-shebangs` hook.

0.9.0 - 2017-07-02
==================
- Add `sort-simple-yaml` hook
- Fix `requirements-txt-fixer` for empty files
- Add `file-contents-sorter` hook for sorting flat files
- `check-merge-conflict` now recognizes rebase conflicts
- Metadata now uses `types` (and therefore requires pre-commit 0.15.0).  This
  allows the text processing hooks to match *all* text files (and to match
  files which would only be classifiable by their shebangs).

0.8.0 - 2017-06-06
==================
- Add flag allowing missing keys to `detect-aws-credentials`
- Handle django default `tests.py` in `name-tests-test`
- Add `--no-ensure-ascii` option to `pretty-format-json`
- Add `no-commit-to-branch` hook

0.7.1 - 2017-02-07
==================
- Don't false positive on files where trailing whitespace isn't changed.

0.7.0 - 2017-01-21
==================
- Improve search for detecting aws keys
- Add .pre-commit-hooks.yaml for forward compatibility

0.6.1 - 2016-11-30
==================
- trailing-whitespace-hook: restore original file on catastrophic failure
- trailing-whitespace-hook: support crlf
- check-yaml: Use safe_load
- check-json: allow custom key sort
- check-json: display filename for non-utf8 files
- New hook: forbid-new-submodules

0.6.0 - 2016-08-12
==================
- Merge conflict detection no longer crashes on binary files
- Indentation in json may be an arbitrary separator
- Editable requirements are properly sorted
- Encoding pragma fixer pragma is configurable

0.5.1 - 2016-05-16
==================
- Add a --no-sort-keys to json pretty formatter
- Add a --remove to fix-encoding-pragma

0.5.0 - 2016-04-05
==================
- Add check-byte-order-marker
- Add check-synlinks
- check-large-files-added understands git-lfs
- Support older git
- Fix regex for --django in test name checker
- Add fix-encoding-pragma hook
- requirements-txt-fixer now sorts like latest pip
- Add check-ast hook
- Add detect-aws-credentials hook
- Allow binary files to pass private key hook
- Add pretty-format-json hook

0.4.2 - 2015-05-31
==================
- Add --django to test name checker
- Add check-merge-conflict hook
- Remove dependency on plumbum
- Add q as a debug statement
- Don't detect markup titles as conflicts
- Teach trailing-whitespace about markdown
- Quickfix for pyflakes - flake8 version conflict

0.4.1 - 2015-03-08
==================
- Respect configuration when running autopep8
- Quickfix for pep8 version conflicts

0.4.0 - 2015-02-22
==================
- Fix trailing-whitespace on OS X
- Add check-added-large-files hook
- Add check-docstring-first hook
- Add requirements-txt-fixer hook
- Add check-case-conflict hook
- Use yaml's CLoader when available in check-yaml for more speed
- Add check-xml hook
- Fix end-of-file-fixer for windows
- Add double-quote-string-fixer hook

0.3.0 - 2014-08-22
==================
- Add autopep8-wrapper hook

0.2.0 - 2014-08-19
==================
- Add check-json hook

0.1.1 - 2014-06-19
==================
- Don't crash on non-parseable files for debug-statement-hook

0.1.0 - 2014-06-07
==================
- Initial Release
