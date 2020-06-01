import argparse
import re
from typing import Optional
from typing import Sequence

CURL_VERBOSE_PATTERN = re.compile(
    br'^(.+)?curl(.+)?((\-v\s)|(\--verbose)|(-w)|(\-\-trace))(.+)?',
)


def _get_file_verbose_occurrences(filename: str) -> int:
    file_verbose_occurrences = 0
    with open(filename, 'rb') as f:
        for i, line in enumerate(f, 1):
            if CURL_VERBOSE_PATTERN.search(line):
                print(
                    f'Talkative/Verbose cURL command found:'
                    f'{repr(filename)}:{repr(i)}:{line.decode("utf-8")}',
                    end='',
                )
                file_verbose_occurrences += 1
    return file_verbose_occurrences


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='File names to check')
    args = parser.parse_args(argv)

    verbose_command_count = 0
    for filename in args.filenames:
        verbose_command_count += _get_file_verbose_occurrences(filename)

    if verbose_command_count > 0:
        print(
            f'Number of talkative/verbose cURL commands:'
            f' {verbose_command_count}',
        )
        return verbose_command_count
    else:
        print('No talkative/verbose cURL commands found!')
        return 0


if __name__ == '__main__':
    exit(main())
