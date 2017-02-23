from __future__ import print_function

import argparse
import sys

import yaml

try:
    from yaml.cyaml import CSafeLoader as Loader
except ImportError:  # pragma: no cover (no libyaml-dev / pypy)
    Loader = yaml.SafeLoader


def check_yaml(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--ignore-tags', type=lambda s: s.split(','), default=[],
                        help='Custom tags to ignore.')
    parser.add_argument('filenames', nargs='*', help='Yaml filenames to check.')
    args = parser.parse_args(argv)

    # Ignore custom tags by returning None
    for tag in args.ignore_tags:
        Loader.add_constructor(tag, lambda *a, **k: None)

    retval = 0
    for filename in args.filenames:
        try:
            yaml.load(open(filename), Loader=Loader)
        except yaml.YAMLError as exc:
            print(exc)
            retval = 1
    return retval


if __name__ == '__main__':
    sys.exit(check_yaml())
