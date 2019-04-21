from __future__ import print_function

import argparse
import collections
import io
import sys
from typing import Any
from typing import Generator
from typing import Optional
from typing import Sequence

import ruamel.yaml

yaml = ruamel.yaml.YAML(typ='safe')


def _exhaust(gen):  # type: (Generator[str, None, None]) -> None
    for _ in gen:
        pass


def _parse_unsafe(*args, **kwargs):  # type: (*Any, **Any) -> None
    _exhaust(yaml.parse(*args, **kwargs))


def _load_all(*args, **kwargs):  # type: (*Any, **Any) -> None
    _exhaust(yaml.load_all(*args, **kwargs))


Key = collections.namedtuple('Key', ('multi', 'unsafe'))
LOAD_FNS = {
    Key(multi=False, unsafe=False): yaml.load,
    Key(multi=False, unsafe=True): _parse_unsafe,
    Key(multi=True, unsafe=False): _load_all,
    Key(multi=True, unsafe=True): _parse_unsafe,
}


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--multi', '--allow-multiple-documents', action='store_true',
    )
    parser.add_argument(
        '--unsafe', action='store_true',
        help=(
            'Instead of loading the files, simply parse them for syntax.  '
            'A syntax-only check enables extensions and unsafe contstructs '
            'which would otherwise be forbidden.  Using this option removes '
            'all guarantees of portability to other yaml implementations.  '
            'Implies --allow-multiple-documents'
        ),
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    load_fn = LOAD_FNS[Key(multi=args.multi, unsafe=args.unsafe)]

    retval = 0
    for filename in args.filenames:
        try:
            with io.open(filename, encoding='UTF-8') as f:
                load_fn(f)
        except ruamel.yaml.YAMLError as exc:
            print(exc)
            retval = 1
    return retval


if __name__ == '__main__':
    sys.exit(main())
