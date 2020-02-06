from pre_commit_hooks import check_unicode_replacement_char


def test_failure(tmpdir):
    f = tmpdir.join('f.txt')
    f.write_text(str(b'\x80abc', errors='replace'), encoding='utf-8')
    assert check_unicode_replacement_char.main((f.strpath,)) == 1


def test_success(tmpdir):
    f = tmpdir.join('f.txt')
    f.write_text(str(b'\x80abc', errors='backslashreplace'), encoding='utf-8')
    assert check_unicode_replacement_char.main((f.strpath,)) == 0
