from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import sys
import xml.sax


def check_xml(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='XML filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            with io.open(filename, 'rb') as xml_file:
                xml.sax.parse(xml_file, xml.sax.ContentHandler())
        except xml.sax.SAXException as exc:
            print('{0}: Failed to xml parse ({1})'.format(filename, exc))
            retval = 1
    return retval


if __name__ == '__main__':
    sys.exit(check_xml())
