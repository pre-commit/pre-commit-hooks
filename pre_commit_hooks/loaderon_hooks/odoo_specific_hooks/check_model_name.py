# -*- coding: utf-8 -*-
import os
import re

from pre_commit_hooks.loaderon_hooks.util.template_methods.file_bunches_lines_checker_template_method import \
    FileBunchesLinesCheckerTemplateMethod


class ModelNameAttributeChecker(FileBunchesLinesCheckerTemplateMethod):
    def __init__(self, argv):
        super(ModelNameAttributeChecker, self).__init__(argv)
        self.__module_name = ''
        name_attribute_regex = r'^(\t| )*_name = .+'
        self.__name_pattern = re.compile(name_attribute_regex)
        inherit_attribute_regex = r'^(\t| )*_inherit = .+'
        self.__inherit_pattern = re.compile(inherit_attribute_regex)
        self.__name_line = ''
        self.__inherit_line = ''

    def _get_regexp(self):
        super(ModelNameAttributeChecker, self)._get_regexp()
        return r'^(\t| )*class.+'

    def _check_file(self):
        self.__module_name = self._set_module_name()
        super(ModelNameAttributeChecker, self)._check_file()

    def _set_module_name(self):
        models_folder_directory_path = os.path.dirname(self.filename)
        module_directory_path = os.path.dirname(models_folder_directory_path)
        return os.path.basename(module_directory_path)

    def _check_bunch(self):
        super(ModelNameAttributeChecker, self)._check_bunch()
        if self.__name_line and not self.__has_multiple_inheritance():
            self.__check_name()

    def _check_line(self):
        """
        We will use this inherited method (which runs through all file lines) in order to gather lines that are required
        to perform the lines bunch check.
        """
        super(ModelNameAttributeChecker, self)._check_line()
        if self.__name_pattern.match(self._file_line):
            self.__name_line = self._file_line.strip('_name = ')
        if self.__inherit_pattern.match(self._file_line):
            self.__inherit_line = self._file_line.strip('_inherit = ')

    def __has_multiple_inheritance(self):
        return '[' in self.__inherit_line and ',' in self.__inherit_line

    def __check_name(self):
        correct_name_regex = r'[\'\"]' + self.__module_name + r'\..+[\'\"]'
        correct_name_pattern = re.compile(correct_name_regex)
        if not correct_name_pattern.match(self.__name_line):
            self.inform_check_failure(
                'El nombre de modelo {} no incluye como prefijo el nombre del módulo {}.'.format(
                    self.__name_line.strip('_name = '),
                    self.__module_name
                )
            )


def main(argv=None):
    return ModelNameAttributeChecker(argv).run()


if __name__ == '__main__':
    exit(main())
