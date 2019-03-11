from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import subprocess
from typing import Any
from typing import Set


class CalledProcessError(RuntimeError):
    pass


def added_files():  # type: () -> Set[str]
    return set(cmd_output(
        'git', 'diff', '--staged', '--name-only', '--diff-filter=A',
    ).splitlines())


def cmd_output(*cmd, **kwargs):  # type: (*str, **Any) -> str
    retcode = kwargs.pop('retcode', 0)
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode('UTF-8')
    if retcode is not None and proc.returncode != retcode:
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout
