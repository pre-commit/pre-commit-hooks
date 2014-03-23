from setuptools import find_packages
from setuptools import setup

setup(
    name='pre_commit_hooks',
    version='0.0.0',
    packages=find_packages('.', exclude=('tests*', 'testing*')),
    install_requires=[
        'argparse',
        'plumbum',
        'pyflakes',
        'simplejson',
    ],
    entry_points={
        'console_scripts': [
            'debug-statement-hook = pre_commit_hooks.debug_statement_hook:debug_statement_hook',
            'trailing-whitespace-fixer = pre_commit_hooks.trailing_whitespace_fixer:fix_trailing_whitespace',
            'name-tests-test = pre_commit_hooks.tests_should_end_in_test:validate_files',
        ],
    },
)
