from __future__ import annotations

import argparse
import collections
from html.parser import HTMLParser
from typing import Sequence


class ValidationException(Exception):
    pass


class ValidatingHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super(HTMLParser, self).__init__()
        self.stack: collections.deque[str] = collections.deque()

    def handle_starttag(
        self, tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            raise ValidationException(f"no opening tag for </{tag}>")
        opening_tag = self.stack.pop()
        if opening_tag != tag:
            stack = '/'.join(self.stack)
            raise ValidationException(
                f"attempt to close {opening_tag} with {tag} at /{stack}",
            )

    def handle_startendtag(
        self, tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        # append and immediately pop stack
        pass

    def close(self) -> None:
        super().close()
        if self.stack:
            opening_tag = self.stack.pop()
            stack = '/'.join(self.stack)
            raise ValidationException(
                f"EOF reached while {opening_tag} at /{stack} not closed",
            )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames',
        nargs='*',
        help='HTML filenames to check.',
    )
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename, 'rb') as html_file:
                html_parser = ValidatingHTMLParser()
                html_parser.feed(html_file.read().decode('ascii', 'ignore'))
                html_parser.close()
        except ValidationException as exc:
            print(f'{filename}: Failed to parse HTML: ({exc})')
            retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
