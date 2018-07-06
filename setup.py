from setuptools import find_packages
from setuptools import setup


setup(
    name='pre_commit_hooks',
    description='Some out-of-the-box hooks for pre-commit.',
    url='https://github.com/pre-commit/pre-commit-hooks',
    version='1.3.0',

    author='Anthony Sottile',
    author_email='asottile@umich.edu',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages(exclude=('tests*', 'testing*')),
    install_requires=[
        # quickfix to prevent pycodestyle conflicts
        'flake8!=2.5.3',
        'autopep8>=1.3',
        'pyyaml',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'autopep8-wrapper = pre_commit_hooks.autopep8_wrapper:main',
            'check-added-large-files = pre_commit_hooks.check_added_large_files:main',
            'check-ast = pre_commit_hooks.check_ast:check_ast',
            'check-builtin-literals = pre_commit_hooks.check_builtin_literals:main',
            'check-byte-order-marker = pre_commit_hooks.check_byte_order_marker:main',
            'check-case-conflict = pre_commit_hooks.check_case_conflict:main',
            'check-docstring-first = pre_commit_hooks.check_docstring_first:main',
            'check-executables-have-shebangs = pre_commit_hooks.check_executables_have_shebangs:main',
            'check-json = pre_commit_hooks.check_json:check_json',
            'check-merge-conflict = pre_commit_hooks.check_merge_conflict:detect_merge_conflict',
            'check-symlinks = pre_commit_hooks.check_symlinks:check_symlinks',
            'check-vcs-permalinks = pre_commit_hooks.check_vcs_permalinks:main',
            'check-xml = pre_commit_hooks.check_xml:check_xml',
            'check-yaml = pre_commit_hooks.check_yaml:check_yaml',
            'debug-statement-hook = pre_commit_hooks.debug_statement_hook:main',
            'detect-aws-credentials = pre_commit_hooks.detect_aws_credentials:main',
            'detect-private-key = pre_commit_hooks.detect_private_key:detect_private_key',
            'double-quote-string-fixer = pre_commit_hooks.string_fixer:main',
            'end-of-file-fixer = pre_commit_hooks.end_of_file_fixer:end_of_file_fixer',
            'file-contents-sorter = pre_commit_hooks.file_contents_sorter:main',
            'fix-encoding-pragma = pre_commit_hooks.fix_encoding_pragma:main',
            'forbid-new-submodules = pre_commit_hooks.forbid_new_submodules:main',
            'mixed-line-ending = pre_commit_hooks.mixed_line_ending:main',
            'name-tests-test = pre_commit_hooks.tests_should_end_in_test:validate_files',
            'no-commit-to-branch = pre_commit_hooks.no_commit_to_branch:main',
            'pretty-format-json = pre_commit_hooks.pretty_format_json:pretty_format_json',
            'requirements-txt-fixer = pre_commit_hooks.requirements_txt_fixer:fix_requirements_txt',
            'sort-simple-yaml = pre_commit_hooks.sort_simple_yaml:main',
            'trailing-whitespace-fixer = pre_commit_hooks.trailing_whitespace_fixer:main',
        ],
    },
)
