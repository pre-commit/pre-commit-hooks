from pre_commit_hooks.check_yaml import yaml


def test_readme_contains_all_hooks():
    with open('README.md', encoding='UTF-8') as f:
        readme_contents = f.read()
    with open('.pre-commit-hooks.yaml', encoding='UTF-8') as f:
        hooks = yaml.load(f)
    for hook in hooks:
        assert f'`{hook["id"]}`' in readme_contents
