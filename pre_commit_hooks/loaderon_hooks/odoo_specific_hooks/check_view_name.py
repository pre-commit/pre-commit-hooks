# -*- coding: utf-8 -*-
import re

from pre_commit_hooks.loaderon_hooks.odoo_specific_hooks.check_view_fields_order import ViewFieldsOrderChecker


class ViewNameChecker(ViewFieldsOrderChecker):
    def __init__(self, argv):
        super(ViewNameChecker, self).__init__(argv)
        self._name_line = None
        self._model_line = None

    def _perform_check(self):
        self.__make_required_strips()
        correct_name_regex = r'<field name="name">' + self._model_line + \
                             r'\.(search|form|tree|filter)(\.inherit)?<\/field>'
        correct_name_pattern = re.compile(correct_name_regex)
        if not correct_name_pattern.match(self._name_line):
            strip_name_line = self._name_line.strip()
            strip_name_line = strip_name_line.strip('<field name="name">')
            strip_name_line = strip_name_line.strip('</field>')
            self.inform_check_failure("El nombre de la vista {} no cumple el formato {}."
                                      .format(strip_name_line, correct_name_regex))

    def __make_required_strips(self):
        self._model_line = self._model_line.strip()
        self._model_line = self._model_line[20:-8]
        self._name_line = self._name_line.strip()


def main(argv=None):
    return ViewNameChecker(argv).run()


if __name__ == '__main__':
    exit(main())
