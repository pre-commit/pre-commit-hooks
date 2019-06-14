# -*- coding: utf-8 -*-
import re

from pre_commit_hooks.loaderon_hooks.util.template_methods.files_bunches_checker_template_method import \
    FileBunchesCheckerTemplateMethod


class ViewFieldsOrderChecker(FileBunchesCheckerTemplateMethod):
    def __init__(self, argv):
        super(ViewFieldsOrderChecker, self).__init__(argv)
        name_line_regex = r'^(\t| )*<field name="name">.+<\/field>(\t| )*'
        self._name_line_pattern = re.compile(name_line_regex)
        model_line_regex = r'^(\t| )*<field name="model">.+<\/field>(\t| )*'
        self._model_line_pattern = re.compile(model_line_regex)
        self._record_line = None
        self._name_line = None
        self._model_line = None

    def _get_regexp(self):
        super(ViewFieldsOrderChecker, self)._get_regexp()
        return r'^(\t| )*<record id=.+ model="ir.ui.view">(\t| )*'

    def _check_bunch(self):
        super(ViewFieldsOrderChecker, self)._check_bunch()
        self._record_line = self._bunch_of_lines[0].strip()
        self._name_line = self._bunch_of_lines[1]
        self._model_line = self._bunch_of_lines[2]
        self._perform_check()

    def _perform_check(self):
        if not self._name_line_pattern.match(self._name_line):
            self.inform_check_failure("El primer campo (field) declarado en un record de vista debe ser 'name'. "
                                      "Vista: {}".format(self._record_line))
        if not self._model_line_pattern.match(self._model_line):
            self.inform_check_failure("El segundo campo (field) declarado en un record de vista debe ser 'model'. "
                                      "Vista: {}".format(self._record_line))


def main(argv=None):
    return ViewFieldsOrderChecker(argv).run()


if __name__ == '__main__':
    exit(main())
