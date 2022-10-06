from __future__ import annotations

import argparse
import json
from typing import Sequence

from pre_commit_hooks.util_string_fixer import fix_strings_in_file_contents


def fix_strings(filename: str) -> int:
    if not filename.endswith('.ipynb'):
        print(f'{filename}: not a Jupyter notebook file')
        return 1

    try:
        with open(filename) as f:
            notebook_contents = json.load(f)
    except json.JSONDecodeError as exc:
        print(f'{filename}: Failed to load ({exc})')
        return 1
    else:
        cells = notebook_contents['cells']
        return_value = 0
        for cell in cells:
            if cell.get('cell_type') == 'code' and 'source' in cell:
                # Each element in cell['source'] is a string that ends with \n,
                # except for the last element, which is why we don't join by \n
                source_in_1_line = ''.join(cell['source'])
                fixed = fix_strings_in_file_contents(source_in_1_line)
                if fixed != source_in_1_line:
                    fixed_lines = fixed.split('\n')
                    cell['source'] = (
                            [_ + '\n' for _ in fixed_lines[:-1]]
                            + [fixed_lines[-1]]
                    )
                    return_value = 1

        if return_value == 1:
            notebook_contents['cells'] = cells
            with open(filename, 'w') as f:
                json.dump(notebook_contents, f, indent=1)
                # Jupyter notebooks (.ipynb) always ends with a new line
                # but json.dump does not.
                f.write("\n")

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
