from __future__ import annotations

import os
import subprocess
from typing import Any


class CalledProcessError(RuntimeError):
    pass


def added_files() -> set[str]:
    cmd = ('git', 'diff', '--staged', '--name-only', '--diff-filter=A')
    return set(cmd_output(*cmd).splitlines())


def cmd_output(*cmd: str, retcode: int | None = 0, **kwargs: Any) -> str:
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if retcode is not None and proc.returncode != retcode:
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout


def zsplit(s: str) -> list[str]:
    s = s.strip('\0')
    if s:
        return s.split('\0')
    else:
        return []


def get_template_path(path: str) -> str:
    parent_dir = os.path.abspath(os.getcwd())
    return os.path.join(parent_dir, 'templates', path)
