import argparse
from typing import Optional
from typing import Sequence


def _process_file(file_obj: bytes) -> bytes:
    # Test for newline at end of file
    # Empty files will throw IOError here

    while len(file_obj):
        if file_obj[-2:] == b'\r\n':
            if len(file_obj) == 2:
                return b''
            elif file_obj[-3:-2] not in {b'\n', b'\r'}:
                return file_obj
            else:
                file_obj = file_obj[:-2]
        elif file_obj[-1:] in {b'\n', b'\r'}:
            if len(file_obj) == 1:
                return b''
            elif file_obj[-2:-1] not in {b'\n', b'\r'}:
                return file_obj
            else:
                file_obj = file_obj[:-1]
        else:
            return file_obj + b'\n'

    return file_obj


def _fix_file(filename: str) -> bool:
    with open(filename, mode='rb') as file_processed:
        file_content = file_processed.read()
    newcontent = _process_file(file_content)
    if newcontent != file_content:
        with open(filename, mode='wb') as file_processed:
            file_processed.write(newcontent)
        return True
    else:
        return False


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        # Read as binary so we can read byte-by-byte
        if _fix_file(filename):
            print(f'Fixing {filename}')
            retv = 1

    return retv


if __name__ == '__main__':
    exit(main())
