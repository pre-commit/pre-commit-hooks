# -*- coding: utf-8 -*-
"""Checks files locations."""
import os
import re

from pre_commit_hooks.loaderon_hooks.util.string_helpers import matches_any_regexp
from pre_commit_hooks.loaderon_hooks.util.template_methods.file_checker_template_method import FileCheckerTemplateMethod


class LocationChecker(FileCheckerTemplateMethod):
    def _add_arguments_to_parser(self):
        super(LocationChecker, self)._add_arguments_to_parser()
        self.parser.add_argument(
            '-ed', '--directories', action='append',
            help='Directory regex to be added to white list. Can be set multiple times to add'
                 'multiple directories to white list.',
        )
        self.parser.add_argument(
            '-ef', '--files', action='append',
            help="Files regex, separated by a white space, to be added to it's corresponded"
                 "directory's white list. Order of this argument declaration matches order of"
                 "--directories declaration, so as to add files to that directory's files whitelist."
                 "This argument can be therefore be set multiple times so as to match --directories sets.",
        )

    def _check_file(self):
        """Check filename location against enabled directories and their enabled files."""
        self.check_arguments_size_match(self.args.directories, self.args.files)
        file_directory_path = os.path.dirname(self.filename)
        file_name = os.path.basename(self.filename)
        location_enabled = False
        for directory_regexp in self.args.directories:
            pattern = re.compile(directory_regexp)
            if pattern.match(file_directory_path):
                location_enabled = True
                file_enabled = self.file_enabled_for_directory(directory_regexp, file_name)
                if not file_enabled:
                    self.inform_check_failure('El archivo {} no está permitido para el directorio {}'
                                              .format(self.filename, file_directory_path))
        if not location_enabled:
            self.inform_check_failure('El directorio {} no está habilitado'.format(file_directory_path))

    def file_enabled_for_directory(self, directory_regexp, filename):
        directory_position_in_arguments = self.args.directories.index(directory_regexp)
        directory_files_whitelist = self.args.files[directory_position_in_arguments]
        files_reg_expressions = directory_files_whitelist.split(' ')
        return matches_any_regexp(filename, files_reg_expressions)


def main(argv=None):
    return LocationChecker(argv).run()


if __name__ == '__main__':
    exit(main())
