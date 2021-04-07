from pre_commit_hooks.check_vcs_permalinks import main


def test_trivial(tmpdir):
    f = tmpdir.join('f.txt').ensure()
    assert not main((str(f),))


def test_passing(tmpdir):
    f = tmpdir.join('f.txt')
    f.write_binary(
        # permalinks are ok
        b'https://github.com/asottile/test/blob/649e6/foo%20bar#L1\n'
        # tags are ok
        b'https://github.com/asottile/test/blob/1.0.0/foo%20bar#L1\n'
        # links to files but not line numbers are ok
        b'https://github.com/asottile/test/blob/master/foo%20bar\n'
        # regression test for overly-greedy regex
        b'https://github.com/ yes / no ? /blob/master/foo#L1\n',
    )
    assert not main((str(f),))


def test_failing(tmpdir, capsys):
    with tmpdir.as_cwd():
        tmpdir.join('f.txt').write_binary(
            b'https://github.com/asottile/test/blob/master/foo#L1\n'
            b'https://example.com/asottile/test/blob/master/foo#L1\n'
            b'https://example.com/asottile/test/blob/main/foo#L1\n',
        )

        assert main(('f.txt', '--additional-github-domain', 'example.com'))
        out, _ = capsys.readouterr()
        assert out == (
            'f.txt:1:https://github.com/asottile/test/blob/master/foo#L1\n'
            'f.txt:2:https://example.com/asottile/test/blob/master/foo#L1\n'
            'f.txt:3:https://example.com/asottile/test/blob/main/foo#L1\n'
            '\n'
            'Non-permanent github link detected.\n'
            'On any page on github press [y] to load a permalink.\n'
        )
