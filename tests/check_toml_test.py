from pre_commit_hooks.check_toml import main


def test_toml_bad(tmpdir):
    filename = tmpdir.join('f')
    filename.write("""
key = # INVALID

= "no key name"  # INVALID
""")
    ret = main((str(filename),))
    assert ret == 1


def test_toml_good(tmpdir):
    filename = tmpdir.join('f')
    filename.write(
        """
# This is a TOML document.

title = "TOML Example"

[owner]
name = "John"
dob = 1979-05-27T07:32:00-08:00 # First class dates
""",
    )
    ret = main((str(filename),))
    assert ret == 0


def test_toml_good_unicode(tmpdir):
    filename = tmpdir.join('f')
    filename.write_binary('letter = "\N{SNOWMAN}"\n'.encode())
    ret = main((str(filename),))
    assert ret == 0
