# -*- coding: utf-8 -*-
import sys

from pre_commit_hooks.loaderon_hooks.general_hooks.check_branch_name import BranchNameChecker
from pre_commit_hooks.loaderon_hooks.general_hooks.check_class_docstring import ClassDocstringChecker
from pre_commit_hooks.loaderon_hooks.general_hooks.check_line import LinesChecker
from pre_commit_hooks.loaderon_hooks.general_hooks.check_location import LocationChecker
from pre_commit_hooks.loaderon_hooks.general_hooks.check_using_pylint import PylintChecker
from pre_commit_hooks.loaderon_hooks.general_hooks.check_xml_encoding import XMLEncodingChecker
from pre_commit_hooks.loaderon_hooks.odoo_specific_hooks.check_model_name import ModelNameAttributeChecker


def run_model_name_checker():
    sys.argv.append('<filename>')
    return ModelNameAttributeChecker(sys.argv).run()


def run_branch_name_checker():
    sys.argv.append('--regex')
    sys.argv.append('<branch regexp>')
    return BranchNameChecker(sys.argv).run()


def run_docstring_checker():
    sys.argv.append('<filename>')
    return ClassDocstringChecker(sys.argv).run()


def run_line_checker():
    # Multiple checks, one regexp per type of line to check.
    sys.argv.append('--line-to-check')
    sys.argv.append(r'^(\t| )*<field.+')
    sys.argv.append('--line-to-check')
    sys.argv.append(r'^(\t| )*<record.+')
    sys.argv.append('--line-to-check')
    sys.argv.append(r'.+fields.Many2one.+')
    sys.argv.append('--line-to-check')
    sys.argv.append(r'.+fields.One2many.+')
    sys.argv.append('--line-to-check')
    sys.argv.append(r'.+fields.Many2many.+')
    sys.argv.append('--line-to-check')
    sys.argv.append(r'class.+')

    # Regexp for knowing how the line must be in order to be correct.
    sys.argv.append('--regexp-to-match')
    sys.argv.append(r'^(\t| )*<field name=".+"')
    sys.argv.append('--regexp-to-match')
    sys.argv.append(r'^(\t| )*<record id=".+"')
    sys.argv.append('--regexp-to-match')
    sys.argv.append(r'^(\t| )*.+_id = fields.Many2one\(')
    sys.argv.append('--regexp-to-match')
    sys.argv.append(r'^(\t| )*.+_ids = fields.One2many\(')
    sys.argv.append('--regexp-to-match')
    sys.argv.append(r'^(\t| )*.+_ids = fields.Many2many\(')
    sys.argv.append('--regexp-to-match')
    sys.argv.append(r'class ([A-Z]+[a-z0-9]+)+\(models.Model\):')

    sys.argv.append('<filename>')

    return LinesChecker(sys.argv).run()


def run_location_checker():
    # Each line is a directory that allows certain types of files.
    sys.argv.append('--directories')
    sys.argv.append(r'^[^\/]+$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/controllers$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/data$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/i18n$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/models$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/report$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/security$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/static\/img$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/static\/lib\/external_lib$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/static\/src\/js$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/static\/src\/css$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/static\/src\/less$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/static\/src\/xml$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/static\/tests$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*[^\/static]\/tests$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/views$')
    sys.argv.append('--directories')
    sys.argv.append(r'.*\/wizard$')

    # Each line specifies what types of files can be located inside the directory.
    sys.argv.append('--files')
    sys.argv.append(r'__init__.py$ __openerp__.py$')
    sys.argv.append('--files')
    sys.argv.append(r'__init__.py$ .*\.py$ main.py$')
    sys.argv.append('--files')
    sys.argv.append(r'.*_data\.xml$ .*_demo\.xml$')
    sys.argv.append('--files')
    sys.argv.append(r'.*\.po$')
    sys.argv.append('--files')
    sys.argv.append(r'__init__.py$ .*\.py$')
    sys.argv.append('--files')
    sys.argv.append(r'__init__.py$ .*\.py$ .*_views\.xml$ .*_reports\.xml$ .*_templates\.xml$')
    sys.argv.append('--files')
    sys.argv.append(r'ir.model.access.csv$ .*_security\.xml$')
    sys.argv.append('--files')
    sys.argv.append(r'.*\.png$ .*\.jpg$')
    sys.argv.append('--files')
    sys.argv.append(r'.*\$')
    sys.argv.append('--files')
    sys.argv.append(r'.*\.js$')
    sys.argv.append('--files')
    sys.argv.append(r'.*\.css$')
    sys.argv.append('--files')
    sys.argv.append(r'.*\.less$')
    sys.argv.append('--files')
    sys.argv.append(r'.*\.xml$')
    sys.argv.append('--files')
    sys.argv.append(r'.*\.tour\.js$')
    sys.argv.append('--files')
    sys.argv.append(r'__init__.py$ test_.*\.py')
    sys.argv.append('--files')
    sys.argv.append(r'.*_templates\.xml$ .*_views\.xml$')
    sys.argv.append('--files')
    sys.argv.append(r'.*\.py$ .*_views\.xml$')

    sys.argv.append('<filename>')

    return LocationChecker(sys.argv).run()


def run_pylint_checker():
    # What files should we exclude from pylint checker
    sys.argv.append('--exclude')
    sys.argv.append(r'.*(\/)*__openerp__.py$')

    sys.argv.append('<filename>')

    return PylintChecker(sys.argv).run()


def run_xml_encoding():
    # Encoding to be checked
    sys.argv.append('--encoding')
    sys.argv.append(r'<?xml version="1.0" encoding="utf-8"?>')

    sys.argv.append('<filename>')

    return XMLEncodingChecker(sys.argv).run()


def main():
    functions = [run_model_name_checker,
                 run_branch_name_checker,
                 run_docstring_checker,
                 run_line_checker,
                 run_location_checker,
                 # run_pylint_checker, #comment or remove a function no to be tested
                 run_xml_encoding]
    for function in functions:
        sys.argv = []
        print('')
        print('----------------------------------')
        print('Test: ' + function.__name__)
        print('')
        function()


if __name__ == '__main__':
    exit(main())
