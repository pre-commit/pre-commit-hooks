from __future__ import print_function

import argparse
import sys
import yaml


def check_yaml(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Yaml filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            yaml.load(open(filename))
        except yaml.YAMLError as exc:
            print(exc)
            retval = 1
    return retval


if __name__ == '__main__':
    sys.exit(check_yaml())
