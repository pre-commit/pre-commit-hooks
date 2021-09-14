import argparse
import json
import sys
from difflib import unified_diff
from typing import Any
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union


def _get_pretty_format(
        contents: str,
        indent: str,
        ensure_ascii: bool = True,
        sort_keys: bool = True,
        sort_values: Sequence[str] = (),
        top_keys: Sequence[str] = (),
        unique_values: Sequence[str] = (),
) -> str:
    def transform_top_keys(pairs: Sequence[Tuple[str, Any]]) -> Sequence[Tuple[str, Any]]:
        transformed_pairs = []
        before = [pair for pair in pairs if pair[0] in top_keys]
        before = sorted(before, key=lambda x: top_keys.index(x[0]))
        after = [pair for pair in pairs if pair[0] not in top_keys]
        if sort_keys:
            after.sort()
        transformed_pairs.extend(before)
        transformed_pairs.extend(after)
        return transformed_pairs

    def transform_sort_values(pairs: Sequence[Tuple[str, Any]]) -> Sequence[Tuple[str, Any]]:
        if not sort_values:
            return pairs
        transformed_pairs = []
        for (key, value) in pairs:
            if (key not in sort_values  # No sorting requested
                or not isinstance(value, List)  # Value is no list, sorting makes no sense
                or len(set([type(x) for x in value])) > 1  # Only sort if all list entries are of the same type
                or any([isinstance(x, (List, Mapping)) for x in value])  # Only sort if all list entries are no list or mapping
            ):
                transformed_pairs.append((key, value))
                continue
            transformed_pairs.append((key, sorted(value)))
        return transformed_pairs

    def transform_unique_values(pairs: Sequence[Tuple[str, Any]]) -> Sequence[Tuple[str, Any]]:
        if not unique_values:
            return pairs
        print(pairs)
        transformed_pairs = []
        for (key, value) in pairs:
            if (key not in unique_values  # No unification requested
                or not isinstance(value, List)  # Value is no list, unification makes no sense
                or len(set([type(x) for x in value])) > 1  # Only unify if all list entries are of the same type
                or any([isinstance(x, (List, Mapping)) for x in value])  # Only unify if all list entries are no list or mapping
            ):
                transformed_pairs.append((key, value))
                continue
            transformed_pairs.append((key, list(dict.fromkeys(value))))
        return transformed_pairs

    def pairs_first(pairs: Sequence[Tuple[str, Any]]) -> Mapping[str, Any]:
        transformed_pairs = transform_unique_values(pairs)
        transformed_pairs = transform_sort_values(transformed_pairs)
        transformed_pairs = transform_top_keys(transformed_pairs)
        return dict(transformed_pairs)

    load=json.loads(contents, object_pairs_hook=pairs_first)
    json_pretty = json.dumps(
        load,
        indent=indent,
        ensure_ascii=ensure_ascii,
    )
    return f'{json_pretty}\n'


def _autofix(filename: str, new_contents: str) -> None:
    print(f'Fixing file {filename}')
    with open(filename, 'w', encoding='UTF-8') as f:
        f.write(new_contents)


def parse_num_to_int(s: str) -> Union[int, str]:
    """Convert string numbers to int, leaving strings as is."""
    try:
        return int(s)
    except ValueError:
        return s


def parse_topkeys(s: str) -> List[str]:
    return s.split(',')


def parse_sortvalues(s: str) -> List[str]:
    return s.split(',')


def parse_uniquevalues(s: str) -> List[str]:
    return s.split(',')


def get_diff(source: str, target: str, file: str) -> str:
    source_lines = source.splitlines(True)
    target_lines = target.splitlines(True)
    diff = unified_diff(source_lines, target_lines, fromfile=file, tofile=file)
    return ''.join(diff)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--autofix',
        action='store_true',
        dest='autofix',
        help='Automatically fixes encountered not-pretty-formatted files',
    )
    parser.add_argument(
        '--indent',
        type=parse_num_to_int,
        default='2',
        help=(
            'The number of indent spaces or a string to be used as delimiter'
            ' for indentation level e.g. 4 or "\t" (Default: 2)'
        ),
    )
    parser.add_argument(
        '--no-ensure-ascii',
        action='store_true',
        dest='no_ensure_ascii',
        default=False,
        help=(
            'Do NOT convert non-ASCII characters to Unicode escape sequences '
            '(\\uXXXX)'
        ),
    )
    parser.add_argument(
        '--no-sort-keys',
        action='store_true',
        dest='no_sort_keys',
        default=False,
        help='Keep JSON nodes in the same order',
    )
    parser.add_argument(
        '--sort-values',
        type=parse_sortvalues,
        dest='sort_values',
        default=[],
        help='The values of the given dict keys are sorted',
    )
    parser.add_argument(
        '--unique-values',
        type=parse_uniquevalues,
        dest='unique_values',
        default=[],
        help='The values of the given dict keys are are made unique',
    )
    parser.add_argument(
        '--top-keys',
        type=parse_topkeys,
        dest='top_keys',
        default=[],
        help='Ordered list of keys to keep at the top of JSON hashes',
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    status = 0

    for json_file in args.filenames:
        with open(json_file, encoding='UTF-8') as f:
            contents = f.read()

        try:
            pretty_contents = _get_pretty_format(
                contents, args.indent, ensure_ascii=not args.no_ensure_ascii,
                sort_keys=not args.no_sort_keys, sort_values=args.sort_values,
                top_keys=args.top_keys, unique_values=args.unique_values,
            )
        except ValueError:
            print(
                f'Input File {json_file} is not a valid JSON, consider using '
                f'check-json',
            )
            return 1

        if contents != pretty_contents:
            if args.autofix:
                _autofix(json_file, pretty_contents)
            else:
                diff_output = get_diff(contents, pretty_contents, json_file)
                sys.stdout.buffer.write(diff_output.encode())

            status = 1

    return status


if __name__ == '__main__':
    exit(main())
