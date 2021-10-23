import sys
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    hookid, new_hookid, url = argv[:3]
    raise SystemExit(
        f'`{hookid}` has been removed -- use `{new_hookid}` from {url}',
    )


if __name__ == '__main__':
    raise SystemExit(main())
