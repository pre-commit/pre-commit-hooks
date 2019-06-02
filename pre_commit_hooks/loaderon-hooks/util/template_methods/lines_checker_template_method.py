# -*- coding: utf-8 -*-
from abc import abstractmethod

from pre_commit_logic.util.template_methods.file_checker_template_method import FileCheckerTemplateMethod
from pre_commit_logic.util.file_helpers import read_file_lines


class LinesCheckerTemplateMethod(FileCheckerTemplateMethod):
    def __init__(self, argv):
        super(LinesCheckerTemplateMethod, self).__init__(argv)
        self._file_lines = []
        self._file_line = ''
        self._file_line_index = 0

    def _check_file(self):
        self._file_lines = read_file_lines(self.filename)
        self._check_lines()

    def _check_lines(self):
        for self._file_line_index, self._file_line in enumerate(self._file_lines):
            self._check_line()

    @abstractmethod
    def _check_line(self):
        pass
