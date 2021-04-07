import argparse
import json
import os
from typing import Optional
from typing import Sequence

from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r', '--report', type=str,
        default='', help='where to store report',
    )
    parser.add_argument(
        '-c', '--config', type=str,
        default='', help='location of config',
    )
    args = parser.parse_args(argv)
    cwd = os.getcwd()

    report = args.report or None
    config = args.config or None

    if not config:
        _config = os.path.join(cwd, '.gitleaks.toml')
        if os.path.isfile(_config):
            config = _config

    cmd = f'gitleaks --redact --quiet --format=json --path={cwd}'
    report_path = None
    if report:
        report_path = os.path.join(cwd, report)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
    if config:
        cmd += f' --config-path={config}'
    out = []
    # history
    try:
        cmd_output(*cmd.split())
    except CalledProcessError as excp:
        for line in excp.args[3].split('\n'):
            if line:
                out.append(json.loads(line))
    # unstaged
    cmd += ' --unstaged'
    try:
        cmd_output(*cmd.split())
    except CalledProcessError as excp:
        for line in excp.args[3].split('\n'):
            if line:
                out.append(json.loads(line))
    if report:
        with open(report_path, 'w') as f:
            json.dump(out, f)
    if out:
        print(json.dumps(out, indent=4))
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
