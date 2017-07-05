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

```shell-session
$ make test
```

If the tests failed whereas [the ones from the last tag](https://travis-ci.org/pre-commit/pre-commit-hooks) did not, your Git configuration might interfere with `pre-commit-hooks`. In this case, you can ignore your current Git configuration by setting a temporary environment variable:

```shell-session
$ env HOME=/tmp make test
```
