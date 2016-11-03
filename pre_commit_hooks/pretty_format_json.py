from __future__ import print_function

import argparse
import sys
from collections import OrderedDict

import simplejson

class SortableOrderedDict(OrderedDict):
    """Performs an in-place sort of the keys if you want."""
    def sort(*args, **kwds):
        self = args[0]
        args = args[1:]
        if 'key' not in kwds:
            kwds['key'] = lambda x: x[0]
        if len(args):
            raise TypeError('expected no positional arguments got {0}'.format(len(args)))
        sorted_od = sorted([x for x in self.items()], **kwds)
        self.clear()
        self.update(sorted_od)

class TrackedSod(SortableOrderedDict):
    """Tracks instances of the SortableOrderedDict."""
    _instances = []
    def __init__(self, *args, **kwds):
        super(TrackedSod, self).__init__(*args, **kwds)
        self.__track(self)

    @classmethod
    def __track(cls, obj):
        cls._instances.append(obj)


def _get_pretty_format(contents, indent, sort_keys=True, top_keys=[]):
    class KeyToCmp(object):
        def __init__(self, obj, *args):
            self.obj = obj[0]
        def __lt__(self, other):
            if self.obj in top_keys and other.obj in top_keys:
                return top_keys.index(self.obj) < top_keys.index(other.obj)
            elif self.obj in top_keys and other.obj not in top_keys:
                return True
            elif self.obj not in top_keys and other.obj in top_keys:
                return False
            else: 
                return self.obj < other.obj
        def __gt__(self, other):
            if self.obj in top_keys and other.obj in top_keys:
                return top_keys.index(self.obj) > top_keys.index(other.obj)
            elif self.obj in top_keys and other.obj not in top_keys:
                return False
            elif self.obj not in top_keys and other.obj in top_keys:
                return True
            else: 
                return self.obj > other.obj
        def __eq__(self, other):
            if self.obj in top_keys and other.obj in top_keys:
                return top_keys.index(self.obj) == top_keys.index(other.obj)
            elif self.obj in top_keys and other.obj not in top_keys:
                return False
            elif self.obj not in top_keys and other.obj in top_keys:
                return False
            else: 
                return self.obj == other.obj
        def __le__(self, other):
            if self.obj in top_keys and other.obj in top_keys:
                return top_keys.index(self.obj) <= top_keys.index(other.obj)
            elif self.obj in top_keys and other.obj not in top_keys:
                return True
            elif self.obj not in top_keys and other.obj in top_keys:
                return False
            else: 
                return self.obj <= other.obj
        def __ge__(self, other):
            if self.obj in top_keys and other.obj in top_keys:
                return top_keys.index(self.obj) >= top_keys.index(other.obj)
            elif self.obj in top_keys and other.obj not in top_keys:
                return False
            elif self.obj not in top_keys and other.obj in top_keys:
                return True
            else: 
                return self.obj >= other.obj
        def __ne__(self, other):
            if self.obj in top_keys and other.obj in top_keys:
                return top_keys.index(self.obj) != top_keys.index(other.obj)
            elif self.obj in top_keys and other.obj not in top_keys:
                return False
            elif self.obj not in top_keys and other.obj in top_keys:
                return False
            else: 
                return self.obj != other.obj
    py_obj = simplejson.loads(contents, object_pairs_hook=TrackedSod)
    if sort_keys:
        for tsod in TrackedSod._instances:
            tsod.sort(key=KeyToCmp)
    # dumps don't end with a newline
    return simplejson.dumps(py_obj, indent=indent) + "\n"

def _autofix(filename, new_contents):
    print("Fixing file {0}".format(filename))
    with open(filename, 'w') as f:
        f.write(new_contents)


def parse_indent(s):
    # type: (str) -> str
    try:
        int_indentation_spec = int(s)
    except ValueError:
        if not s.strip():
            return s
        else:
            raise ValueError(
                'Non-whitespace JSON indentation delimiter supplied. ',
            )
    else:
        if int_indentation_spec >= 0:
            return int_indentation_spec * ' '
        else:
            raise ValueError(
                'Negative integer supplied to construct JSON indentation delimiter. ',
            )

def parse_topkeys(s):
    # type: (str) -> array
    return s.split(',')

def pretty_format_json(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--autofix',
        action='store_true',
        dest='autofix',
        help='Automatically fixes encountered not-pretty-formatted files',
    )
    parser.add_argument(
        '--indent',
        type=parse_indent,
        default='  ',
        help='String used as delimiter for one indentation level',
    )
    parser.add_argument(
        '--no-sort-keys',
        action='store_true',
        dest='no_sort_keys',
        default=False,
        help='Keep JSON nodes in the same order',
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
        with open(json_file) as f:
            contents = f.read()

        try:
            pretty_contents = _get_pretty_format(
                contents, args.indent, sort_keys=not args.no_sort_keys,
                top_keys=args.top_keys
            )

            if contents != pretty_contents:
                print("File {0} is not pretty-formatted".format(json_file))

                if args.autofix:
                    _autofix(json_file, pretty_contents)

                status = 1

        except simplejson.JSONDecodeError:
            print(
                "Input File {0} is not a valid JSON, consider using check-json"
                .format(json_file)
            )
            return 1

    return status


if __name__ == '__main__':
    sys.exit(pretty_format_json())
