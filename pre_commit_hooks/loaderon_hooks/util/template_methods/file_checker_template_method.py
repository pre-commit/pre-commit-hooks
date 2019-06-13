# -*- coding: utf-8 -*-
from abc import abstractmethod

from pre_commit_hooks.loaderon_hooks.util.template_methods.checker_template_method import CheckerTemplateMethod


class FileCheckerTemplateMethod(CheckerTemplateMethod):
    def __init__(self, argv):
        super(FileCheckerTemplateMethod, self).__init__(argv)
        self.filename = ''

    def _add_arguments_to_parser(self):
        super(FileCheckerTemplateMethod, self)._add_arguments_to_parser()
        self.parser.add_argument('filenames', nargs='*')

    def _perform_checks(self):
        super(FileCheckerTemplateMethod, self)._perform_checks()
        """For each file, check it's location."""
        for self.filename in self.args.filenames:
            self._check_file()

    @abstractmethod
    def _check_file(self):
        pass
