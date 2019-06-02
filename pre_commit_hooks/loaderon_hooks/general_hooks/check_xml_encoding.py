# -*- coding: utf-8 -*-
from pre_commit_hooks.loaderon_hooks.util.file_helpers import read_file_line
from pre_commit_hooks.loaderon_hooks.util.template_methods.file_checker_template_method import FileCheckerTemplateMethod


class XMLEncodingChecker(FileCheckerTemplateMethod):
    def _add_arguments_to_parser(self):
        super(XMLEncodingChecker, self)._add_arguments_to_parser()
        self.parser.add_argument('-e', '--encoding', help='Desired encoding.')

    def _check_file(self):
        first_line = read_file_line(self.filename)
        desired_encoding = self.args.encoding.rstrip()
        first_line = first_line.rstrip('\n')
        if first_line != desired_encoding:
            self.inform_check_failure(
                'El archivo {} no comienza con la línea "{}" (verifica también espacios en blanco)'.format(
                    self.filename,
                    desired_encoding
                )
            )


def main(argv=None):
    return XMLEncodingChecker(argv).run()


if __name__ == '__main__':
    exit(main())
