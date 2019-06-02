# -*- coding: utf-8 -*-
import re

from pre_commit_hooks.loaderon_hooks.util.template_methods.lines_checker_template_method import \
    LinesCheckerTemplateMethod


class LinesChecker(LinesCheckerTemplateMethod):
    def _add_arguments_to_parser(self):
        super(LinesChecker, self)._add_arguments_to_parser()
        self.parser.add_argument('-l', '--line-to-check', action='append', help='Regex to check.')
        self.parser.add_argument('-r', '--regexp-to-match', action='append', help='Regex to match.')

    def _check_arguments(self):
        self.check_arguments_size_match(self.args.line_to_check, self.args.regexp_to_match)

    def _check_line(self):
        for line_index, line_to_check in enumerate(self.args.line_to_check):
            line_to_check_pattern = re.compile(line_to_check)
            if line_to_check_pattern.match(self._file_line):
                line_regexp_to_match = self.args.regexp_to_match[line_index]
                correct_pattern = re.compile(line_regexp_to_match)
                if not correct_pattern.match(self._file_line):
                    self.inform_check_failure(
                        "Una de las líneas con '{}' no está correctamente formulada. Línea {}: \n\n{}\n"
                        "Debería cumplir la expresión regular: {}".format(
                            line_to_check,
                            self._file_line_index + 1,
                            self._file_line,
                            line_regexp_to_match
                        )
                    )


def main(argv=None):
    return LinesChecker(argv).run()


if __name__ == '__main__':
    exit(main())
