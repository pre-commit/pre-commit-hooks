#!/usr/bin/env python3
"""This is a script to install git-lfs to a tempdir for use in tests"""
import io
import os.path
import shutil
import tarfile
from urllib.request import urlopen

DOWNLOAD_PATH = (
    'https://github.com/github/git-lfs/releases/download/'
    'v2.2.1/git-lfs-linux-amd64-2.2.1.tar.gz'
)
PATH_IN_TAR = 'git-lfs-2.2.1/git-lfs'
DEST_PATH = '/tmp/git-lfs/git-lfs'
DEST_DIR = os.path.dirname(DEST_PATH)


def main():
    if (
            os.path.exists(DEST_PATH) and
            os.path.isfile(DEST_PATH) and
            os.access(DEST_PATH, os.X_OK)
    ):
        print('Already installed!')
        return 0

    shutil.rmtree(DEST_DIR, ignore_errors=True)
    os.makedirs(DEST_DIR, exist_ok=True)

    contents = io.BytesIO(urlopen(DOWNLOAD_PATH).read())
    with tarfile.open(fileobj=contents) as tar:
        with tar.extractfile(PATH_IN_TAR) as src_file:
            with open(DEST_PATH, 'wb') as dest_file:
                shutil.copyfileobj(src_file, dest_file)
    os.chmod(DEST_PATH, 0o755)


if __name__ == '__main__':
    exit(main())
