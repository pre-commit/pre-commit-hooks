# -*- coding: utf-8 -*-
"""Executes Pylint checks on all git modified and added files."""
import re

from pylint.lint import Run
from pylint.reporters.text import TextReporter

from pre_commit_hooks.loaderon_hooks.util.file_helpers import find_file_starting_from_reference_file_directory
from pre_commit_hooks.loaderon_hooks.util.template_methods.file_checker_template_method import FileCheckerTemplateMethod


class PylintChecker(FileCheckerTemplateMethod):
    def __init__(self, argv):
        super(PylintChecker, self).__init__(argv)
        self.pylint_output = WritableObject()

    def _add_arguments_to_parser(self):
        super(PylintChecker, self)._add_arguments_to_parser()
        self.parser.add_argument('-e', '--exclude', help='Excluded files to check.')

    def _check_file(self):
        try:
            self.run_pylint_except_in_excluded_files()
        except SystemExit as exception:
            self.manage_pylint_result(exception)

    def run_pylint_except_in_excluded_files(self):
        excluded_files_regex = self.args.exclude
        pattern = re.compile(excluded_files_regex)
        if not pattern.match(self.filename):
            self.run_pylint_on_file()

    def run_pylint_on_file(self):
        """Runs pylint with .pylint config file if found, default config otherwise."""
        pylint_configuration_file = find_file_starting_from_reference_file_directory(__file__, '.pylintrc')
        if pylint_configuration_file:
            Run(['--rcfile', pylint_configuration_file, self.filename], reporter=TextReporter(self.pylint_output))
        else:
            Run([self.filename], reporter=TextReporter(self.pylint_output))

    def manage_pylint_result(self, exception):
        print(self.pylint_output.read())
        if exception.code != 0:
            self.inform_check_failure('')


class WritableObject(object):
    """Simple writable object for pylint."""

    def __init__(self):
        self.__content = ''

    def write(self, line):
        """Adds line to object content."""
        self.__content = self.__content + '\n' + line

    def read(self):
        """Returns object content."""
        return self.__content


def main(argv=None):
    return PylintChecker(argv).run()


if __name__ == '__main__':
    exit(main())
