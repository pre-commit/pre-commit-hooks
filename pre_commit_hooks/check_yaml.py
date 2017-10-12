from __future__ import print_function

import argparse
import sys

import yaml

try:
    from yaml.cyaml import CSafeLoader as Loader
except ImportError:  # pragma: no cover (no libyaml-dev / pypy)
    Loader = yaml.SafeLoader


def _load_all(*args, **kwargs):
    # need to exhaust the generator
    return tuple(yaml.load_all(*args, **kwargs))


def check_yaml(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--allow-multiple-documents', dest='yaml_load_fn',
        action='store_const', const=_load_all, default=yaml.load,
    )
    parser.add_argument('filenames', nargs='*', help='Yaml filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            args.yaml_load_fn(open(filename), Loader=Loader)
        except yaml.YAMLError as exc:
            print(exc)
            retval = 1
    return retval


if __name__ == '__main__':
    sys.exit(check_yaml())
