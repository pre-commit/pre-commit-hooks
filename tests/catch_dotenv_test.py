from __future__ import annotations

import os
import re
import shutil
import threading
import time
from pathlib import Path

import pytest

from pre_commit_hooks.catch_dotenv import DEFAULT_ENV_FILE
from pre_commit_hooks.catch_dotenv import DEFAULT_EXAMPLE_ENV_FILE
from pre_commit_hooks.catch_dotenv import DEFAULT_GITIGNORE_FILE
from pre_commit_hooks.catch_dotenv import ensure_env_in_gitignore
from pre_commit_hooks.catch_dotenv import GITIGNORE_BANNER
from pre_commit_hooks.catch_dotenv import main

# Tests cover hook behavior: detection gating, .gitignore normalization,
# example file generation parsing edge cases, idempotency, and preservation of
# existing content. Each test isolates a single behavioral contract.


@pytest.fixture()
def env_file(tmp_path: Path) -> Path:
    """Copy shared resource .env into tmp workspace as the canonical .env.

    All tests rely on this baseline content (optionally appending extra lines
    for edge cases) to ensure consistent parsing behavior.
    """
    # Find repository root by looking for .git directory
    test_file_path = Path(__file__).resolve()
    repo_root = test_file_path
    while repo_root.parent != repo_root:  # Stop at filesystem root
        if (repo_root / '.git').exists():
            break
        repo_root = repo_root.parent
    else:
        raise RuntimeError('Could not find repository root (.git directory)')

    # Source file stored as test.env in repo (cannot commit a real .env in CI)
    resource_env = repo_root / 'testing' / 'resources' / 'test.env'
    dest = tmp_path / DEFAULT_ENV_FILE
    shutil.copyfile(resource_env, dest)
    return dest


def run_hook(
        tmp_path: Path, staged: list[str], create_example: bool = False,
) -> int:
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        args = staged[:]
        if create_example:
            args.append('--create-example')
        return main(args)
    finally:
        os.chdir(cwd)


def test_no_env_file(tmp_path: Path, env_file: Path) -> None:
    """Hook should no-op (return 0) if .env not staged even if it exists."""
    (tmp_path / 'foo.txt').write_text('x')
    assert run_hook(tmp_path, ['foo.txt']) == 0


def test_blocks_env_and_updates_gitignore(
        tmp_path: Path, env_file: Path,
) -> None:
    """Staging .env triggers block (exit 1) and appends banner + env entry."""
    ret = run_hook(tmp_path, [DEFAULT_ENV_FILE])
    assert ret == 1
    gi = (tmp_path / DEFAULT_GITIGNORE_FILE).read_text().splitlines()
    assert gi[-2] == GITIGNORE_BANNER
    assert gi[-1] == DEFAULT_ENV_FILE


def test_env_present_but_not_staged(tmp_path: Path, env_file: Path) -> None:
    """Existing .env on disk but not staged should not block commit."""
    assert run_hook(tmp_path, ['unrelated.txt']) == 0


def test_idempotent_gitignore(tmp_path: Path, env_file: Path) -> None:
    """Re-running after initial normalization leaves .gitignore unchanged."""
    g = tmp_path / DEFAULT_GITIGNORE_FILE
    g.write_text(f"{GITIGNORE_BANNER}\n{DEFAULT_ENV_FILE}\n")
    first = run_hook(tmp_path, [DEFAULT_ENV_FILE])
    assert first == 1
    content1 = g.read_text()
    second = run_hook(tmp_path, [DEFAULT_ENV_FILE])
    assert second == 1
    assert g.read_text() == content1  # unchanged


def test_gitignore_with_existing_content_preserved(
        tmp_path: Path, env_file: Path,
) -> None:
    """Existing entries stay intact; banner/env appended at end cleanly."""
    g = tmp_path / DEFAULT_GITIGNORE_FILE
    g.write_text(
        'node_modules/\n# comment line\n',
    )  # existing content with trailing newline
    run_hook(tmp_path, [DEFAULT_ENV_FILE])
    lines = g.read_text().splitlines()
    # original content should still be at top
    assert lines[0] == 'node_modules/'
    assert '# comment line' in lines[1]
    # Last two lines should be banner + env file
    assert lines[-2:] == [GITIGNORE_BANNER, DEFAULT_ENV_FILE]


def test_gitignore_duplicates_are_collapsed(
        tmp_path: Path, env_file: Path,
) -> None:
    """Multiple prior duplicate banner/env lines collapse to single pair."""
    g = tmp_path / DEFAULT_GITIGNORE_FILE
    g.write_text(
        f"other\n{GITIGNORE_BANNER}\n{DEFAULT_ENV_FILE}\n"
        f"{GITIGNORE_BANNER}\n{DEFAULT_ENV_FILE}\n\n\n",
    )
    run_hook(tmp_path, [DEFAULT_ENV_FILE])
    lines = g.read_text().splitlines()
    assert lines.count(GITIGNORE_BANNER) == 1
    assert lines.count(DEFAULT_ENV_FILE) == 1
    assert lines[-2:] == [GITIGNORE_BANNER, DEFAULT_ENV_FILE]


def test_create_example(tmp_path: Path, env_file: Path) -> None:
    """Example file includes discovered keys; values stripped to KEY=."""
    ret = run_hook(tmp_path, [DEFAULT_ENV_FILE], create_example=True)
    assert ret == 1
    example = (tmp_path / DEFAULT_EXAMPLE_ENV_FILE).read_text().splitlines()
    key_lines = [ln for ln in example if ln and not ln.startswith('#')]
    # All key lines should be KEY=
    assert all(re.match(r'^[A-Za-z_][A-Za-z0-9_]*=$', ln) for ln in key_lines)
    # Spot check a few known keys from resource file
    for k in [
        'OPENAI_API_KEY=',
        'ACCESS_TOKEN_SECRET=',
        'SUPABASE_SERVICE_KEY=',
    ]:
        assert k in key_lines


def test_create_example_duplicate_key_variant_ignored(
        tmp_path: Path, env_file: Path,
) -> None:
    """Appending whitespace duplicate of existing key should not duplicate
    in example.
    """
    # Create a copy of the env_file to avoid contaminating the fixture
    modified_env = tmp_path / 'modified.env'
    shutil.copyfile(env_file, modified_env)
    with open(modified_env, 'a', encoding='utf-8') as f:
        f.write('BACKEND_CONTAINER_PORT =999 # duplicate variant\n')

    # Override the env file path for this test
    original_env = tmp_path / DEFAULT_ENV_FILE
    shutil.copyfile(modified_env, original_env)
    run_hook(tmp_path, [DEFAULT_ENV_FILE], create_example=True)
    lines = (tmp_path / DEFAULT_EXAMPLE_ENV_FILE).read_text().splitlines()
    key_lines = [ln for ln in lines if ln and not ln.startswith('#')]
    assert key_lines.count('BACKEND_CONTAINER_PORT=') == 1


def test_gitignore_without_trailing_newline(
        tmp_path: Path, env_file: Path,
) -> None:
    """Normalization works when original .gitignore lacks trailing newline."""
    g = tmp_path / DEFAULT_GITIGNORE_FILE
    g.write_text('existing_line')  # no newline at EOF
    run_hook(tmp_path, [DEFAULT_ENV_FILE])
    lines = g.read_text().splitlines()
    assert lines[0] == 'existing_line'
    assert lines[-2:] == [GITIGNORE_BANNER, DEFAULT_ENV_FILE]


def test_ensure_env_in_gitignore_normalizes(
        tmp_path: Path, env_file: Path,
) -> None:
    """Direct API call collapses duplicates and produces canonical tail
    layout.
    """
    g = tmp_path / DEFAULT_GITIGNORE_FILE
    g.write_text(
        f"{GITIGNORE_BANNER}\n{DEFAULT_ENV_FILE}\n"
        f"{GITIGNORE_BANNER}\n{DEFAULT_ENV_FILE}\n\n",
    )
    modified = ensure_env_in_gitignore(
        DEFAULT_ENV_FILE, str(g), GITIGNORE_BANNER,
    )
    assert modified is True
    lines = g.read_text().splitlines()
    # final two lines should be banner + env
    assert lines[-2:] == [GITIGNORE_BANNER, DEFAULT_ENV_FILE]
    # only one occurrence each
    assert lines.count(GITIGNORE_BANNER) == 1
    assert lines.count(DEFAULT_ENV_FILE) == 1


def test_source_env_file_not_modified(
        tmp_path: Path, env_file: Path,
) -> None:
    """Hook must not alter original .env (comments and formatting stay)."""
    original = env_file.read_text()
    run_hook(tmp_path, [DEFAULT_ENV_FILE], create_example=True)
    assert env_file.read_text() == original


def test_large_resource_env_parsing(
        tmp_path: Path, env_file: Path,
) -> None:
    """Generate example from resource env; assert broad key coverage &
    format.
    """
    ret = run_hook(tmp_path, [DEFAULT_ENV_FILE], create_example=True)
    assert ret == 1
    example_lines = (
        (tmp_path / DEFAULT_EXAMPLE_ENV_FILE).read_text().splitlines()
    )
    key_lines = [ln for ln in example_lines if ln and not ln.startswith('#')]
    assert len(key_lines) > 20
    assert all(re.match(r'^[A-Za-z_][A-Za-z0-9_]*=$', ln) for ln in key_lines)
    for k in [
        'BACKEND_CONTAINER_PORT=',
        'SUPABASE_SERVICE_KEY=',
        'ACCESS_TOKEN_SECRET=',
    ]:
        assert k in key_lines


def test_failure_message_content(
        tmp_path: Path,
        env_file: Path,
        capsys: pytest.CaptureFixture[str],
) -> None:
    """Hook stdout message should contain key phrases when blocking commit."""
    ret = run_hook(tmp_path, [DEFAULT_ENV_FILE], create_example=True)
    assert ret == 1
    out = capsys.readouterr().out.strip()
    assert 'Blocked committing' in out
    assert DEFAULT_GITIGNORE_FILE in out  # updated path appears
    assert 'Generated .env.example.' in out
    assert 'Remove .env' in out


def test_create_example_when_env_missing(
        tmp_path: Path, env_file: Path,
) -> None:
    """--create-example with no .env staged or present should no-op (exit 0).

    Uses env_file fixture (requirement: all tests use fixture) then removes the
    copied .env to simulate absence.
    """
    env_file.unlink()
    ret = run_hook(tmp_path, ['unrelated.txt'], create_example=True)
    assert ret == 0
    assert not (tmp_path / DEFAULT_EXAMPLE_ENV_FILE).exists()


def test_gitignore_is_directory_error(
        tmp_path: Path,
        env_file: Path,
        capsys: pytest.CaptureFixture[str],
) -> None:
    """If .gitignore path is a directory, hook should print error and still
    block.
    """
    gitignore_dir = tmp_path / DEFAULT_GITIGNORE_FILE
    gitignore_dir.mkdir()
    ret = run_hook(tmp_path, [DEFAULT_ENV_FILE])
    assert ret == 1  # still blocks commit
    captured = capsys.readouterr()
    assert 'ERROR:' in captured.err  # error now printed to stderr


def test_env_example_overwrites_existing(
        tmp_path: Path, env_file: Path,
) -> None:
    """Pre-existing example file with junk should be overwritten with header
    & keys.
    """
    example = tmp_path / DEFAULT_EXAMPLE_ENV_FILE
    example.write_text('junk=1\nSHOULD_NOT_REMAIN=2\n')
    run_hook(tmp_path, [DEFAULT_ENV_FILE], create_example=True)
    content = example.read_text().splitlines()
    assert content[0].startswith('# Generated by catch-dotenv')
    assert any(ln.startswith('BACKEND_CONTAINER_PORT=') for ln in content)
    assert 'junk=1' not in content
    assert 'SHOULD_NOT_REMAIN=2' not in content


def test_large_gitignore_normalization_performance(
        tmp_path: Path, env_file: Path,
) -> None:
    """Very large .gitignore remains normalized quickly (functional smoke)."""
    g = tmp_path / DEFAULT_GITIGNORE_FILE
    # Generate many lines with scattered duplicates of banner/env
    lines = (
        [f"file_{i}" for i in range(3000)] +
        [GITIGNORE_BANNER, DEFAULT_ENV_FILE] * 3
    )
    g.write_text('\n'.join(lines) + '\n')
    start = time.time()
    run_hook(tmp_path, [DEFAULT_ENV_FILE])
    elapsed = time.time() - start
    result_lines = g.read_text().splitlines()
    assert result_lines[-2:] == [GITIGNORE_BANNER, DEFAULT_ENV_FILE]
    assert result_lines.count(GITIGNORE_BANNER) == 1
    assert result_lines.count(DEFAULT_ENV_FILE) == 1
    # Soft performance expectation: should finish fast
    # (< 0.5s on typical dev machine)
    assert elapsed < 0.5


def test_concurrent_gitignore_writes(
        tmp_path: Path, env_file: Path,
) -> None:
    """Concurrent ensure_env_in_gitignore calls result in canonical final
    state.
    """
    g = tmp_path / DEFAULT_GITIGNORE_FILE
    # Seed with messy duplicates
    g.write_text(f"other\n{GITIGNORE_BANNER}\n{DEFAULT_ENV_FILE}\n\n")

    def worker():
        ensure_env_in_gitignore(DEFAULT_ENV_FILE, str(g), GITIGNORE_BANNER)

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    lines = g.read_text().splitlines()
    assert lines[-2:] == [GITIGNORE_BANNER, DEFAULT_ENV_FILE]
    assert lines.count(GITIGNORE_BANNER) == 1
    assert lines.count(DEFAULT_ENV_FILE) == 1


def test_mixed_staged_files(
        tmp_path: Path, env_file: Path,
) -> None:
    """Staging .env with other files still blocks and only normalizes
    gitignore once.
    """
    other = tmp_path / 'README.md'
    other.write_text('hi')
    ret = run_hook(tmp_path, [DEFAULT_ENV_FILE, 'README.md'])
    assert ret == 1
    lines = (tmp_path / DEFAULT_GITIGNORE_FILE).read_text().splitlines()
    assert lines[-2:] == [GITIGNORE_BANNER, DEFAULT_ENV_FILE]


def test_already_ignored_env_with_variations(
        tmp_path: Path, env_file: Path,
) -> None:
    """Pre-existing ignore lines with spacing normalize to single
    canonical pair.
    """
    g = tmp_path / DEFAULT_GITIGNORE_FILE
    g.write_text(
        f"  {DEFAULT_ENV_FILE}  \n{GITIGNORE_BANNER}\n"
        f"   {DEFAULT_ENV_FILE}\n",
    )
    run_hook(tmp_path, [DEFAULT_ENV_FILE])
    lines = g.read_text().splitlines()
    assert lines[-2:] == [GITIGNORE_BANNER, DEFAULT_ENV_FILE]
    assert lines.count(DEFAULT_ENV_FILE) == 1


def test_subdirectory_invocation(
        tmp_path: Path, env_file: Path,
) -> None:
    """Running from a subdirectory now writes .gitignore relative to CWD
    (simplified behavior).
    """
    sub = tmp_path / 'subdir'
    sub.mkdir()
    # simulate repository root marker
    (tmp_path / '.git').mkdir()
    # simulate running hook from subdir while staged path relative to repo root
    cwd = os.getcwd()
    os.chdir(sub)
    try:
        ret = main(
            [str(Path('..') / DEFAULT_ENV_FILE)],
        )  # staged path relative to subdir
        gi = (sub / DEFAULT_GITIGNORE_FILE).read_text().splitlines()
    finally:
        os.chdir(cwd)
    assert ret == 1
    assert gi[-2:] == [GITIGNORE_BANNER, DEFAULT_ENV_FILE]


def test_atomic_write_failure_gitignore(
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        env_file: Path,
        capsys: pytest.CaptureFixture[str],
) -> None:
    """Simulate os.replace failure during gitignore write to exercise error
    path.
    """
    def boom(*_a: object, **_k: object) -> None:
        raise OSError('replace-fail')
    monkeypatch.setattr('pre_commit_hooks.catch_dotenv.os.replace', boom)
    modified = ensure_env_in_gitignore(
        DEFAULT_ENV_FILE,
        str(tmp_path / DEFAULT_GITIGNORE_FILE),
        GITIGNORE_BANNER,
    )
    assert modified is False
    captured = capsys.readouterr()
    assert 'ERROR: unable to write' in captured.err


def test_atomic_write_failure_example(
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        env_file: Path,
        capsys: pytest.CaptureFixture[str],
) -> None:
    """Simulate os.replace failure when writing example env file."""
    def boom(*_a: object, **_k: object) -> None:
        raise OSError('replace-fail')
    monkeypatch.setattr('pre_commit_hooks.catch_dotenv.os.replace', boom)
    ok = False
    # create_example_env requires source .env to exist; env_file fixture
    # provides it in tmp_path root
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        ok = main([DEFAULT_ENV_FILE, '--create-example']) == 1
    finally:
        os.chdir(cwd)
    # hook still blocks; but example creation failed -> message should
    # not claim Example file generated
    assert ok is True
    captured = capsys.readouterr()
    out = captured.out
    err = captured.err
    assert 'Example file generated' not in out
    assert 'ERROR: unable to write' in err


def test_atomic_write_cleanup_failure(
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        env_file: Path,
) -> None:
    """Test rare case where os.remove fails during cleanup after os.replace
    failure.
    """
    def failing_remove(_path: str) -> None:
        # Simulate os.remove failure during cleanup
        raise OSError('remove-fail')

    def failing_replace(*_a: object, **_k: object) -> None:
        # First fail os.replace to trigger cleanup path
        raise OSError('replace-fail')

    monkeypatch.setattr(
        'pre_commit_hooks.catch_dotenv.os.replace', failing_replace,
    )
    monkeypatch.setattr(
        'pre_commit_hooks.catch_dotenv.os.remove', failing_remove,
    )

    # This should not raise an exception even if both replace and remove fail
    modified = ensure_env_in_gitignore(
        DEFAULT_ENV_FILE,
        str(tmp_path / DEFAULT_GITIGNORE_FILE),
        GITIGNORE_BANNER,
    )
    assert modified is False


def test_create_example_read_error(
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        env_file: Path,
        capsys: pytest.CaptureFixture[str],
) -> None:
    """Test OSError when reading source env file for create_example."""
    def failing_open(*_args: object, **_kwargs: object) -> None:
        raise OSError('Permission denied')

    # Mock open to fail when trying to read the env file
    monkeypatch.setattr('builtins.open', failing_open)

    from pre_commit_hooks.catch_dotenv import create_example_env

    result = create_example_env(str(env_file), str(tmp_path / 'test.example'))
    assert result is False

    captured = capsys.readouterr()
    assert 'ERROR: unable to read' in captured.err


def test_malformed_env_lines_ignored(tmp_path: Path, env_file: Path) -> None:
    """Test that malformed env lines that don't match regex are ignored."""
    # Create env file with malformed lines
    malformed_env = tmp_path / 'malformed.env'
    malformed_content = [
        'VALID_KEY=value',
        'invalid-line-no-equals',
        '# comment line',
        '',  # empty line
        '=INVALID_EQUALS_FIRST',
        'ANOTHER_VALID=value2',
        'spaces in key=invalid',
        '123_INVALID_START=value',  # starts with number
    ]
    malformed_env.write_text('\n'.join(malformed_content))

    # Copy to .env location
    shutil.copyfile(malformed_env, tmp_path / DEFAULT_ENV_FILE)

    # Run create-example - should only extract valid keys
    run_hook(tmp_path, [DEFAULT_ENV_FILE], create_example=True)

    example_lines = (
        (tmp_path / DEFAULT_EXAMPLE_ENV_FILE).read_text().splitlines()
    )
    key_lines = [ln for ln in example_lines if ln and not ln.startswith('#')]

    # Should only have the valid keys
    assert 'VALID_KEY=' in key_lines
    assert 'ANOTHER_VALID=' in key_lines
    assert len([k for k in key_lines if '=' in k]) == 2  # Only 2 valid keys


def test_create_example_when_source_missing(
        tmp_path: Path, env_file: Path,
) -> None:
    """Test --create-example when source .env doesn't exist but .env is
    staged.
    """
    # Remove the source .env file but keep it in the staged files list
    env_file.unlink()  # Remove the .env file

    # Stage .env even though it doesn't exist on disk
    ret = run_hook(tmp_path, [DEFAULT_ENV_FILE], create_example=True)

    # Hook should still block commit
    assert ret == 1

    # But no example file should be created since source doesn't exist
    assert not (tmp_path / DEFAULT_EXAMPLE_ENV_FILE).exists()
