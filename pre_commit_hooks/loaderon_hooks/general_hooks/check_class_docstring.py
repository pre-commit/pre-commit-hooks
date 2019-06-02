# -*- coding: utf-8 -*-
import re

from pre_commit_hooks.loaderon_hooks.util.template_methods.lines_checker_template_method import \
    LinesCheckerTemplateMethod


class ClassDocstringChecker(LinesCheckerTemplateMethod):
    def _check_line(self):
        regular_expression = r'^(\t| )*class .+\(.*\):'
        pattern = re.compile(regular_expression)
        if pattern.match(self._file_line):
            self.__check_class_docstring(self._file_line_index)

    def __check_class_docstring(self, class_line_index):
        class_first_line = self._file_lines[class_line_index + 1]
        if class_first_line in ['\n', '\r\n']:
            self.inform_check_failure('El docstring de la clase {} está separado de su clase por una o más líneas en '
                                      'blanco.'.format(self._file_lines[class_line_index]))
        if not class_first_line.strip().startswith('\"\"\"'):
            self.inform_check_failure('La clase {} no tiene docstring.'.format(self._file_lines[class_line_index]))


def main(argv=None):
    return ClassDocstringChecker(argv).run()


if __name__ == '__main__':
    exit(main())
