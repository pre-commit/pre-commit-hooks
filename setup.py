from setuptools import find_packages
from setuptools import setup

setup(
    name='pre_commit_hooks',
    version='0.0.0',
    packages=find_packages('.', exclude=('tests*', 'testing*')),
    install_requires=[
        'argparse',
        'pyflakes',
        'simplejson',
    ],
)
