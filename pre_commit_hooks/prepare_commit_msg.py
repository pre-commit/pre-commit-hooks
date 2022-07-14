from __future__ import annotations

import argparse
import re
from typing import Sequence

from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape

from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output


def get_current_branch() -> str:
    try:
        ref_name = cmd_output('git', 'symbolic-ref', '--short', 'HEAD')
    except CalledProcessError:
        return ''

    return ref_name.strip()


def _configure_args(
        parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
    parser.add_argument(
        '-t', '--template', default='prepare_commit_msg_append.j2',
        help='Template to use for the commit message.',
    )
    parser.add_argument(
        '-b', '--branch', action='append', default=['main', 'master'],
        help='Branch to skip, may be specified multiple times.',
    )
    parser.add_argument(
        '-p', '--pattern', action='append', default=['(?<=feature/).*'],
        help='RegEx Pattern for recognising Ticket Numbers in branch, '
             'may be specified multiple times.',
    )
    parser.add_argument('COMMIT_MSG_FILE', nargs=argparse.REMAINDER)

    return parser


def get_jinja_env() -> Environment:
    return Environment(
        loader=PackageLoader('pre_commit_hooks'),
        autoescape=select_autoescape(),
    )


def get_rendered_template(
        jinja: Environment,
        template_file: str,
        variables: dict[str, str],
) -> str:
    template = jinja.get_template(template_file)
    return template.render(variables)


def update_commit_file(
        jinja: Environment,
        commit_msg_file: str,
        template: str,
        ticket: str,
) -> int:
    try:
        with open(commit_msg_file) as f:
            data = f.readlines()

        data_as_str = ''.join([item for item in data])
        # if message already contain ticket number means
        # it is under git commit --amend or rebase or alike
        # where message was already set in the past
        if ticket in data_as_str:
            return 0

        variables = {
            'ticket': ticket,
            'content': data_as_str,
        }

        content = get_rendered_template(
            jinja=jinja,
            template_file=template,
            variables=variables,
        )
        with open(commit_msg_file, 'w') as f:
            f.write(content)

        return 0
    except OSError as err:
        print(f'OS error: {err}')
        return 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = _configure_args(argparse.ArgumentParser())
    args = parser.parse_args(argv)

    current = get_current_branch()
    branches = frozenset(args.branch)
    if current in branches:
        # checked black listed branches
        return 0

    patterns = frozenset(args.pattern)
    matches = [
        match.group(0)
        for match in (re.search(pattern, current) for pattern in patterns)
        if match
    ]
    if len(matches) == 0:
        # checked white listed branches
        return 0

    jinja = get_jinja_env()
    commit_file = args.COMMIT_MSG_FILE[0]
    return update_commit_file(jinja, commit_file, args.template, matches[0])


if __name__ == '__main__':
    raise SystemExit(main())
