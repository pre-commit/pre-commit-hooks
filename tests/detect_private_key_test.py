import pytest

from pre_commit_hooks.detect_private_key import detect_private_key

# Input, expected return value
TESTS = (
    (b'-----BEGIN RSA PRIVATE KEY-----', 1),
    (b'-----BEGIN DSA PRIVATE KEY-----', 1),
    (b'-----BEGIN EC PRIVATE KEY-----', 1),
    (b'-----BEGIN OPENSSH PRIVATE KEY-----', 1),
    (b'PuTTY-User-Key-File-2: ssh-rsa', 1),
    (b'---- BEGIN SSH2 ENCRYPTED PRIVATE KEY ----', 1),
    (b'ssh-rsa DATA', 0),
    (b'ssh-dsa DATA', 0),
    # Some arbitrary binary data
    (b'\xa2\xf1\x93\x12', 0),
)


@pytest.mark.parametrize(('input_s', 'expected_retval'), TESTS)
def test_detect_private_key(input_s, expected_retval, tmpdir):
    path = tmpdir.join('file.txt')
    path.write_binary(input_s)
    assert detect_private_key([path.strpath]) == expected_retval
