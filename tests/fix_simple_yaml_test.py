from __future__ import absolute_import
from __future__ import unicode_literals

from pre_commit_hooks import fix_yaml


def test_no_change(tmpdir):
    f = tmpdir.join('f.yaml')
    f.write('---\nfoo: bar')
    assert fix_yaml.main((f.strpath,)) == 0


def test_change(tmpdir):
    f = tmpdir.join('f.yaml')
    f.write('foo: bar')
    assert fix_yaml.main((f.strpath,)) == 1
