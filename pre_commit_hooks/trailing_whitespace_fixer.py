
import argparse
import sys
from plumbum import local


def fix_trailing_whitespace(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    bad_whitespace_files = filter(bool, local['grep'][
        ('-l', '[[:space:]]$') + tuple(args.filenames)
    ](retcode=None).splitlines())

    if bad_whitespace_files:
        for bad_whitespace_file in bad_whitespace_files:
            print 'Fixing {0}'.format(bad_whitespace_file)
            local['sed']['-i', '-e', 's/[[:space:]]*$//', bad_whitespace_file]()
        return 1
    else:
        return 0


def entry():
    fix_trailing_whitespace(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(entry())
