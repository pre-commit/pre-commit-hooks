from setuptools import find_packages
from setuptools import setup


setup(
    name='pre_commit_hooks',
    description='Some out-of-the-box hooks for pre-commit.',
    url='https://github.com/pre-commit/pre-commit-hooks',
    version='2.1.0',

    author='Anthony Sottile',
    author_email='asottile@umich.edu',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages(exclude=('tests*', 'testing*')),
    install_requires=[
        'flake8',
        'ruamel.yaml>=0.15',
        'six',
    ],
    extras_require={':python_version<"3.5"': ['typing']},
    entry_points={
        'console_scripts': [
            'autopep8-wrapper = pre_commit_hooks.autopep8_wrapper:main',
            'check-added-large-files = pre_commit_hooks.check_added_large_files:main',  # noqa: E501
            'check-ast = pre_commit_hooks.check_ast:main',
            'check-builtin-literals = pre_commit_hooks.check_builtin_literals:main',  # noqa: E501
            'check-byte-order-marker = pre_commit_hooks.check_byte_order_marker:main',  # noqa: E501
            'check-case-conflict = pre_commit_hooks.check_case_conflict:main',
            'check-docstring-first = pre_commit_hooks.check_docstring_first:main',  # noqa: E501
            'check-executables-have-shebangs = pre_commit_hooks.check_executables_have_shebangs:main',  # noqa: E501
            'check-json = pre_commit_hooks.check_json:main',
            'check-merge-conflict = pre_commit_hooks.check_merge_conflict:main',  # noqa: E501
            'check-symlinks = pre_commit_hooks.check_symlinks:main',
            'check-vcs-permalinks = pre_commit_hooks.check_vcs_permalinks:main',  # noqa: E501
            'check-xml = pre_commit_hooks.check_xml:main',
            'check-yaml = pre_commit_hooks.check_yaml:main',
            'debug-statement-hook = pre_commit_hooks.debug_statement_hook:main',  # noqa: E501
            'detect-aws-credentials = pre_commit_hooks.detect_aws_credentials:main',  # noqa: E501
            'detect-private-key = pre_commit_hooks.detect_private_key:main',
            'double-quote-string-fixer = pre_commit_hooks.string_fixer:main',
            'end-of-file-fixer = pre_commit_hooks.end_of_file_fixer:main',
            'file-contents-sorter = pre_commit_hooks.file_contents_sorter:main',  # noqa: E501
            'fix-encoding-pragma = pre_commit_hooks.fix_encoding_pragma:main',
            'forbid-new-submodules = pre_commit_hooks.forbid_new_submodules:main',  # noqa: E501
            'mixed-line-ending = pre_commit_hooks.mixed_line_ending:main',
            'name-tests-test = pre_commit_hooks.tests_should_end_in_test:main',
            'no-commit-to-branch = pre_commit_hooks.no_commit_to_branch:main',
            'pretty-format-json = pre_commit_hooks.pretty_format_json:main',
            'requirements-txt-fixer = pre_commit_hooks.requirements_txt_fixer:main',  # noqa: E501
            'sort-simple-yaml = pre_commit_hooks.sort_simple_yaml:main',
            'trailing-whitespace-fixer = pre_commit_hooks.trailing_whitespace_fixer:main',  # noqa: E501
        ],
    },
)
