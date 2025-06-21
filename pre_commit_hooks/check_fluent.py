from __future__ import annotations

import argparse
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename, encoding='UTF-8') as f:
                content = f.read()

            if not _validate_fluent_syntax(content, filename):
                retval = 1

        except (OSError, UnicodeDecodeError) as exc:
            print(f"{filename}: Failed to read file ({exc})")
            retval = 1

    return retval


def _validate_fluent_syntax(content: str, filename: str) -> bool:
    """Validate Fluent FTL file syntax."""
    lines = content.splitlines()
    errors = []

    # Track current message context
    current_message = None
    has_default_variant = False
    in_select_expression = False

    for line_num, line in enumerate(lines, 1):
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith('#'):
            continue

        # Check for message definitions (identifier = value)
        if (
            '=' in line and
            not line.startswith(' ') and
            not line.startswith('\t')
        ):
            current_message = line.split('=')[0].strip()
            in_select_expression = False
            has_default_variant = False

            # Validate message identifier
            if not _is_valid_identifier(current_message):
                errors.append(
                    f"Line {line_num}: Invalid message identifier "
                    f'"{current_message}"',
                )

            # Check for select expressions (contains -> or other select syntax)
            if '{' in line and '$' in line and '->' in line:
                in_select_expression = True

        # Handle indented content (attributes, variants, multiline values)
        elif line.startswith(' ') or line.startswith('\t'):
            if current_message is None:
                errors.append(
                    f"Line {line_num}: Indented content without "
                    f"message context",
                )
                continue

            stripped = line.strip()

            # Check for attribute definitions
            if stripped.startswith('.') and '=' in stripped:
                # Remove leading dot
                attr_name = stripped.split('=')[0].strip()[1:]
                if not _is_valid_identifier(attr_name):
                    errors.append(
                        f"Line {line_num}: Invalid attribute identifier "
                        f'"{attr_name}"',
                    )

            # Check for variants in select expressions
            elif stripped.startswith('*') or (
                stripped.startswith('[') and stripped.endswith(']')
            ):
                if not in_select_expression:
                    errors.append(
                        f"Line {line_num}: Variant definition outside "
                        f"select expression",
                    )
                elif stripped.startswith('*'):
                    has_default_variant = True
                else:
                    # Non-* variants don't set has_default_variant
                    pass

        # Check for unterminated select expressions
        if in_select_expression and current_message:
            if '}' in line:
                in_select_expression = False
                if not has_default_variant:
                    errors.append(
                        f"Line {line_num}: Select expression missing "
                        f"default variant (marked with *)",
                    )

    # Report errors
    if errors:
        for error in errors:
            print(f"{filename}: {error}")
        return False

    return True


def _is_valid_identifier(identifier: str) -> bool:
    """Check if identifier follows Fluent naming conventions."""
    if not identifier:
        return False

    # Must start with letter
    if not identifier[0].isalpha():
        return False

    # Can contain letters, numbers, underscores, and hyphens
    for char in identifier:
        if not (char.isalnum() or char in '_-'):
            return False

    return True


if __name__ == '__main__':
    raise SystemExit(main())
