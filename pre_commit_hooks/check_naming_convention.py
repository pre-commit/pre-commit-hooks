from __future__ import annotations

import os
import re
import sys


def check_naming_convention(files):
    for file_path in files:
        with open(file_path) as file:
            lines = file.readlines()
            for line_num, line in enumerate(lines, start=1):
                words = re.findall(r'\b[a-zA-Z0-9_]+\b', line)
                for word in words:
                    if re.match(r'^[a-z]+(?:_[a-z]+)*$', word):
                        continue  # Valid snake_case
                    elif re.match(r'^[A-Z][a-zA-Z0-9]*$', word):
                        if '_' in word:
                            print(f'WARNING: CamelCase with underscores found in {os.path.basename(file_path)}:{line_num}: {word}')
                        continue  # Valid CamelCase
                    else:
                        print(f'ERROR: Invalid naming convention in {os.path.basename(file_path)}:{line_num}: {word}')
                        sys.exit(1)
