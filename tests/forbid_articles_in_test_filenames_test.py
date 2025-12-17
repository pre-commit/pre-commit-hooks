from __future__ import annotations

import subprocess
import sys
from pathlib import Path


HOOK = Path(__file__).parents[1] / 'pre_commit_hooks' / 'forbid_articles_in_test_filenames.py'


def run_hook(repo_path: Path):
    """Run the hook in a temporary git repo and return (exit_code, stdout)."""
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout.strip()


def init_git_repo(tmp_path: Path):
    subprocess.run(['git', 'init'], cwd=tmp_path, check=True)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=tmp_path, check=True)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=tmp_path, check=True)


def git_add_all(tmp_path: Path):
    subprocess.run(['git', 'add', '.'], cwd=tmp_path, check=True)


def test_fails_on_forbidden_article_in_test_filename(tmp_path: Path):
    init_git_repo(tmp_path)

    bad_test = tmp_path / 'tests_create_an_address.py'
    bad_test.write_text('def test_something(): pass\n')

    git_add_all(tmp_path)

    code, output = run_hook(tmp_path)

    assert code == 1
    assert 'ERROR: Forbidden article in test filename:' in output
    assert 'tests_create_an_address.py' in output


def test_passes_on_valid_test_filename(tmp_path: Path):
    init_git_repo(tmp_path)

    good_test = tmp_path / 'tests_create_address.py'
    good_test.write_text('def test_something(): pass\n')

    git_add_all(tmp_path)

    code, output = run_hook(tmp_path)

    assert code == 0
    assert output == ''
