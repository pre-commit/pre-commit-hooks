from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re
import sys

DT_MANIPULATION_RE = re.compile(
    r'[+-]=?\s?datetime.timedelta\(|[+-]=?\s?timedelta\(|.replace\(.*tzinfo=|datetime\(.*tzinfo=',
)


def _check_file(filename):
    return_value = 0
    with open(filename, 'r') as f:
        for i, line in enumerate(f, 1):
            if DT_MANIPULATION_RE.search(line):
                if line.strip().endswith('  # safe_dt_op') or line.strip().startswith('#'):
                    continue

                sys.stdout.write('{}:{}: {}'.format(filename, i, line))
                sys.stdout.flush()

                return_value += 1

    return return_value


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    return_value = 0
    for filename in args.filenames:
        result = _check_file(filename)
        return_value |= 1 if result > 0 else 0

    return return_value


if __name__ == '__main__':
    exit(main())
