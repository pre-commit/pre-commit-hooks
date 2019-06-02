# -*- coding: utf-8 -*-
import re

from pre_commit_logic.util.template_methods.checker_template_method import CheckerTemplateMethod
from pre_commit_logic.util.git_helpers import get_current_branch_name


class BranchNameChecker(CheckerTemplateMethod):
    def _add_arguments_to_parser(self):
        self.parser.add_argument('-r', '--regex', help='Regex that git current branch must match.')

    def _perform_checks(self):
        regular_expression = self.args.regex
        pattern = re.compile(regular_expression)
        current_branch_name = get_current_branch_name()
        if not pattern.match(current_branch_name):
            self.inform_check_failure('El nombre de la rama debe ser del estilo {}'.format(regular_expression))


def main(argv=None):
    return BranchNameChecker(argv).run()


if __name__ == '__main__':
    exit(main())
