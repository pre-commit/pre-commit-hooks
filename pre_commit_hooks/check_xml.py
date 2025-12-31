from __future__ import annotations

import argparse
import xml.sax.handler
from collections.abc import Sequence

import defusedxml

defusedxml.defuse_stdlib()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='XML filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    handler = xml.sax.handler.ContentHandler()
    for filename in args.filenames:
        try:
            with open(filename, 'rb') as xml_file:
                defusedxml.sax.parse(xml_file, handler)
        except xml.sax.SAXException as exc:
            print(f'{filename}: Failed to xml parse ({exc})')
            retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
