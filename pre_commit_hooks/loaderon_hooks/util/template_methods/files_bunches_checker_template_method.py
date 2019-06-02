# -*- coding: utf-8 -*-
from abc import abstractmethod

from pre_commit_hooks.loaderon_hooks.util.file_helpers import split_by_regexp
from pre_commit_hooks.loaderon_hooks.util.template_methods.file_checker_template_method import FileCheckerTemplateMethod


class FileBunchesCheckerTemplateMethod(FileCheckerTemplateMethod):
    def __init__(self, argv):
        super(FileBunchesCheckerTemplateMethod, self).__init__(argv)
        self._bunch_of_lines = []

    def _check_file(self):
        regexp = self._get_regexp()
        bunches_of_lines = split_by_regexp(self.filename, regexp)
        for self._bunch_of_lines in bunches_of_lines:
            self._check_bunch()

    @abstractmethod
    def _get_regexp(self):
        pass

    @abstractmethod
    def _check_bunch(self):
        pass
