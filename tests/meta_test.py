import io


def test_hooks_yaml_same_contents():
    legacy_contents = io.open('hooks.yaml').read()
    contents = io.open('.pre-commit-hooks.yaml').read()
    assert legacy_contents == contents
