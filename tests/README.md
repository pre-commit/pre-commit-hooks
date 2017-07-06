Testing
=======

Installing the test environment
-------------------------------

### Debian-based distributions

```shell-session
$ sudo apt install pypy python2.7 python3.5 python3.6 python-tox
```

Running the tests
-----------------

### Running the complete test suite

```shell-session
$ make test
```

If the tests failed whereas [the ones from the last tag](https://travis-ci.org/pre-commit/pre-commit-hooks) did not, your Git configuration might interfere with `pre-commit-hooks`. In this case, you can ignore your current Git configuration by setting a temporary environment variable:

```shell-session
$ env HOME=/tmp make test
```

### Running only a specific test

If you are developing a new hook or adding features to an existing one, you may want to run the tests for that particular hook. The following command will run the wanted test on every supported Python version.

```shell-session
$ tox tests/<your_test>.py
```

If you want to run your test for a specific Python version (for a quicker execution), you can specify it with the `-e` option of `tox`. At the moment, the supported Python versions are `2.7` (`-e py27`), `3.4` (`-e py34`), and `3.5` (`-e py35`). For example:

```shell-session
$ tox -e py27 tests/<your_test>.py
```

You can run your specific test ignoring your own Git configuration like so:

```shell-session
$ env HOME=/tmp tox -e py27 tests/<your_test>.py
```
