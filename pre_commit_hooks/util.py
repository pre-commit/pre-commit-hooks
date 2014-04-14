import functools
import sys


def entry(func):
    """Allows a function that has `argv` as an argument to be used as a
    commandline entry.  This will make the function callable using either
    explicitly passed argv or defaulting to sys.argv[1:]
    """
    @functools.wraps(func)
    def wrapper(argv=None):
        if argv is None:
            argv = sys.argv[1:]
        return func(argv)
    return wrapper
