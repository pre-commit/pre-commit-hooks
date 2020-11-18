import subprocess
from typing import Any
from typing import List
from typing import Optional
from typing import Set


class CalledProcessError(RuntimeError):
    pass


def added_files() -> Set[str]:
    cmd = ('git', 'diff', '--staged', '--name-only', '--diff-filter=A')
    return set(cmd_output(*cmd).splitlines())


def cmd_output(*cmd: str, retcode: Optional[int] = 0, **kwargs: Any) -> str:
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if retcode is not None and proc.returncode != retcode:
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout


def zsplit(s: str) -> List[str]:
    s = s.strip('\0')
    if s:
        return s.split('\0')
    else:
        return []
