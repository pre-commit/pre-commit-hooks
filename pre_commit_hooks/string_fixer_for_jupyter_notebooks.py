from __future__ import annotations

import argparse
import json
from typing import Sequence

from pre_commit_hooks.util_string_fixer import fix_strings_in_file_contents


def fix_strings(filename: str) -> int:
    with open(filename) as f:
        notebook_contents = json.load(f)

    cells = notebook_contents['cells']
    return_value = 0
    for cell in cells:
        if cell['cell_type'] == 'code':
            source_in_1_line = ''.join(cell['source'])
            fixed = fix_strings_in_file_contents(source_in_1_line)
            if fixed != source_in_1_line:
                fixed_lines = fixed.split('\n')
                cell['source'] = [_ + '\n' for _ in fixed_lines[:-1]] + [fixed_lines[-1]]
                return_value = 1

    if return_value == 1:
        notebook_contents['cells'] = cells
        with open(filename, 'w') as f:
            json.dump(notebook_contents, f, indent=1)
            f.write("\n")  # because json.dump doesn't put \n at the end

    return return_value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        return_value = fix_strings(filename)
        if return_value != 0:
            print(f'Fixing strings in {filename}')
        retv |= return_value

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
