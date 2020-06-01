from pre_commit_hooks.detect_verbose_curl import main


def test_trivial(tmpdir):
    f = tmpdir.join('f.sh').ensure()
    assert not main((str(f),))


def test_passing(tmpdir):
    f = tmpdir.join('f.sh')
    f.write_binary(
        b'#!/usr/bin/env bash\n'
        # setup
        b'url=https://api.somesite.com\n'
        # api call 1
        b'curl -X GET ${url} -H "X-Custom-Header: pytest-test"\n'
        # api call 2
        b'curl -d "{key1:value1, key2:value2}" -H '
        b'"Content-Type: application/json" -X POST ${url} \n'
        # test comments
        b'# None of these commands have curl verbose - '
        b'this comment should NOT be recognised as -- is missing\n'
        b'# The "trace" amd other options should also not be picked up.\n '
        # list the version of curl - should not be picked up. Only
        b'curl --version\n'
        b'curl -V\n',
    )
    assert main((str(f),)) == 0


def test_failing(tmpdir, capsys):
    with tmpdir.as_cwd():
        tmpdir.join('f.sh').write_binary(
            b'#!/usr/bin/env bash\n'
            # setup
            b'url=https://api.somesite.com\n'
            # Talkative cURL HTTP calls
            b'curl -v -X GET ${url} -H "X-Custom-Header: pytest-test"\n'
            b'curl -X GET ${url} -H '
            b'"X-Custom-Header: pytest-test" --verbose\n'
            b'curl --write-out output.txt -X GET ${url} '
            b'-H "X-Custom-Header: pytest-test"\n',
        )
        tmpdir.join('f.groovy').write_binary(
            b'#!/usr/bin/env bash\n'
            # setup
            b'url=https://api.somesite.com\n'
            # Talkative cURL HTTP calls
            b'curl -d "{key1:value1, key2:value2}" -w output.txt '
            b'-H "Content-Type: application/json" -X POST ${url}\n'
            b'curl --trace-ascii ascii.txt -d "{key1:value1, key2:value2}" '
            b'-H "Content-Type: application/json" -X POST ${url}\n'
            b'curl -d "{key1:value1, key2:value2}" -X POST ${url} '
            b'--trace trace.txt  -H "Content-Type: application/json"\n',
        )

        assert main(('f.sh', 'f.groovy')) == 6

        out, _ = capsys.readouterr()
        assert out == (
            "Talkative/Verbose cURL command found:'f.sh':3:curl -v -X GET"
            " ${url} -H \"X-Custom-Header: pytest-test\"\n"
            "Talkative/Verbose cURL command found:'f.sh':4:curl -X GET "
            "${url} -H \"X-Custom-Header: pytest-test\" --verbose\n"
            'Talkative/Verbose cURL command found:'
            "'f.sh':5:curl --write-out output.txt"
            " -X GET ${url} -H \"X-Custom-Header: pytest-test\"\n"

            "Talkative/Verbose cURL command found:'f.groovy':3:curl "
            "-d \"{key1:value1, key2:value2}\""
            " -w output.txt -H \"Content-Type: application/json\""
            ' -X POST ${url}\n'
            'Talkative/Verbose cURL command found:'
            "'f.groovy':4:curl "
            '--trace-ascii ascii.txt '
            "-d \"{key1:value1, key2:value2}\""
            " -H \"Content-Type: application/json\" "
            '-X POST ${url}\n'
            "Talkative/Verbose cURL command found:'f.groovy':5:curl "
            "-d \"{key1:value1, key2:value2}\""
            ' -X POST ${url} --trace trace.txt '
            " -H \"Content-Type: application/json\"\n"

            'Number of talkative/verbose cURL commands: 6\n'
        )
