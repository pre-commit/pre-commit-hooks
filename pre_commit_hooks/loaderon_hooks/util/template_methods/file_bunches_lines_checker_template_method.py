# -*- coding: utf-8 -*-
from abc import abstractmethod

from pre_commit_logic.util.template_methods.files_bunches_checker_template_method import \
    FileBunchesCheckerTemplateMethod
from pre_commit_logic.util.template_methods.lines_checker_template_method import LinesCheckerTemplateMethod


class FileBunchesLinesCheckerTemplateMethod(FileBunchesCheckerTemplateMethod, LinesCheckerTemplateMethod):
    @abstractmethod
    def _get_regexp(self):
        pass

    def _check_bunch(self):
        """
        This method uses LinesCheckerTemplateMethod's _check_lines. Which receives self._file_lines. In this case, our
        'file lines' will be the bunches of lines got by split_by_classes.
        """
        self._file_lines = self._bunch_of_lines
        self._check_lines()

    @abstractmethod
    def _check_line(self):
        pass
