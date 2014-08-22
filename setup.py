from setuptools import find_packages
from setuptools import setup


setup(
    name='pre_commit_hooks',
    description='Some out-of-the-box hooks for pre-commit.',
    url='https://github.com/pre-commit/pre-commit-hooks',
    version='0.3.0',

    author='Anthony Sottile',
    author_email='asottile@umich.edu',

    platforms='linux',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages('.', exclude=('tests*', 'testing*')),
    install_requires=[
        'argparse',
        'autopep8',
        'flake8',
        'plumbum',
        'pyflakes',
        'pyyaml',
        'simplejson',
    ],
    entry_points={
        'console_scripts': [
            'autopep8-wrapper = pre_commit_hooks.autopep8_wrapper:main',
            'check-json = pre_commit_hooks.check_json:check_json',
            'check-yaml = pre_commit_hooks.check_yaml:check_yaml',
            'debug-statement-hook = pre_commit_hooks.debug_statement_hook:debug_statement_hook',
            'end-of-file-fixer = pre_commit_hooks.end_of_file_fixer:end_of_file_fixer',
            'name-tests-test = pre_commit_hooks.tests_should_end_in_test:validate_files',
            'trailing-whitespace-fixer = pre_commit_hooks.trailing_whitespace_fixer:fix_trailing_whitespace',
        ],
    },
)
