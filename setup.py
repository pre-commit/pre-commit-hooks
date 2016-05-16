from setuptools import find_packages
from setuptools import setup


setup(
    name='pre_commit_hooks',
    description='Some out-of-the-box hooks for pre-commit.',
    url='https://github.com/pre-commit/pre-commit-hooks',
    version='0.5.1',

    author='Anthony Sottile',
    author_email='asottile@umich.edu',

    platforms='linux',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages('.', exclude=('tests*', 'testing*')),
    install_requires=[
        # quickfix to prevent pep8 conflicts
        'flake8!=2.5.3',
        'argparse',
        'autopep8>=1.1',
        'pyyaml',
        'simplejson',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'autopep8-wrapper = pre_commit_hooks.autopep8_wrapper:main',
            'check-added-large-files = pre_commit_hooks.check_added_large_files:main',
            'check-ast = pre_commit_hooks.check_ast:check_ast',
            'check-byte-order-marker = pre_commit_hooks.check_byte_order_marker:main',
            'check-case-conflict = pre_commit_hooks.check_case_conflict:main',
            'check-docstring-first = pre_commit_hooks.check_docstring_first:main',
            'check-json = pre_commit_hooks.check_json:check_json',
            'check-merge-conflict = pre_commit_hooks.check_merge_conflict:detect_merge_conflict',
            'check-symlinks = pre_commit_hooks.check_symlinks:check_symlinks',
            'check-xml = pre_commit_hooks.check_xml:check_xml',
            'check-yaml = pre_commit_hooks.check_yaml:check_yaml',
            'debug-statement-hook = pre_commit_hooks.debug_statement_hook:debug_statement_hook',
            'detect-aws-credentials = pre_commit_hooks.detect_aws_credentials:main',
            'detect-private-key = pre_commit_hooks.detect_private_key:detect_private_key',
            'double-quote-string-fixer = pre_commit_hooks.string_fixer:main',
            'end-of-file-fixer = pre_commit_hooks.end_of_file_fixer:end_of_file_fixer',
            'fix-encoding-pragma = pre_commit_hooks.fix_encoding_pragma:main',
            'name-tests-test = pre_commit_hooks.tests_should_end_in_test:validate_files',
            'pretty-format-json = pre_commit_hooks.pretty_format_json:pretty_format_json',
            'requirements-txt-fixer = pre_commit_hooks.requirements_txt_fixer:fix_requirements_txt',
            'trailing-whitespace-fixer = pre_commit_hooks.trailing_whitespace_fixer:fix_trailing_whitespace',
        ],
    },
)
