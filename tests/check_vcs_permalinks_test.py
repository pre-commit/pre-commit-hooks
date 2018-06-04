from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from pre_commit_hooks.check_vcs_permalinks import main


def test_trivial(tmpdir):
    f = tmpdir.join('f.txt').ensure()
    assert not main((f.strpath,))


def test_passing(tmpdir):
    f = tmpdir.join('f.txt')
    f.write_binary(
        # permalinks are ok
        b'https://github.com/asottile/test/blob/649e6/foo%20bar#L1\n'
        # links to files but not line numbers are ok
        b'https://github.com/asottile/test/blob/master/foo%20bar\n',
    )
    assert not main((f.strpath,))


@pytest.mark.parametrize(
    'contents',
    (
        'http://github.com/asottile/test/blob/master/foo#L1',
        'http://www.github.com/asottile/test/blob/master/foo#L1',
        'https://github.com/asottile/test/blob/master/foo#L1',
        'https://www.github.com/asottile/test/blob/master/foo#L1',
        'https://www.github.com/asottile/test/blob/master/foo#my-anchor',
    ),
)
def test_failing(contents, tmpdir, capsys):
    with tmpdir.as_cwd():
        tmpdir.join('f.txt').write_binary(
            '{}\n'.format(contents).encode('utf-8'),
        )

        assert main(('f.txt',))
        out, _ = capsys.readouterr()
        assert out == (
            'f.txt:1:{}\n'
            '\n'
            'Non-permanent github link detected.\n'
            'On any page on github press [y] to load a permalink.\n'.format(contents)
        )
