from setuptools import find_packages
from setuptools import setup

setup(
    name='pre_commit_hooks',
    version='0.0.0',
    packages=find_packages('.', exclude=('tests*', 'testing*')),
    install_requires=[
        'argparse',
        'flake8',
        'plumbum',
        'pyflakes',
        'pyyaml',
        'simplejson',
    ],
    entry_points={
        'console_scripts': [
            'check-yaml = pre_commit_hooks.check_yaml:check_yaml',
            'debug-statement-hook = pre_commit_hooks.debug_statement_hook:debug_statement_hook',
            'end-of-file-fixer = pre_commit_hooks.end_of_file_fixer:end_of_file_fixer',
            'name-tests-test = pre_commit_hooks.tests_should_end_in_test:validate_files',
            'trailing-whitespace-fixer = pre_commit_hooks.trailing_whitespace_fixer:fix_trailing_whitespace',
        ],
    },
)
