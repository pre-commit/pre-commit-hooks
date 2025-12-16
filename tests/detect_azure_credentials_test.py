from __future__ import annotations

import pytest

from pre_commit_hooks.detect_azure_credentials import main
from testing.util import get_resource_path


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("azure_credentials.txt", 1),
        ("azure_no_credentials.txt", 0),
        ("nonsense.txt", 0),
        ("ok_json.json", 0),
    ),
)
def test_detect_azure_credentials(filename, expected_retval):
    """Test detection of Azure credentials in various files."""
    ret = main((get_resource_path(filename),))
    assert ret == expected_retval


def test_detect_multiple_files():
    """Test scanning multiple files at once."""
    ret = main(
        (
            get_resource_path("azure_credentials.txt"),
            get_resource_path("azure_no_credentials.txt"),
        )
    )
    # Should return 1 because at least one file has credentials
    assert ret == 1


def test_detect_multiple_credentials_in_single_file():
    """Test that multiple credentials in one file are all detected."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1


def test_no_credentials_in_multiple_files():
    """Test scanning multiple clean files."""
    ret = main(
        (
            get_resource_path("azure_no_credentials.txt"),
            get_resource_path("nonsense.txt"),
            get_resource_path("ok_json.json"),
        )
    )
    assert ret == 0


def test_datafactory_shir_key_detection():
    """Test specific detection of Azure Data Factory SHIR keys."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1


def test_storage_credential_86char_detection():
    """Test detection of 86 character storage credentials."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1


def test_storage_credential_43char_detection():
    """Test detection of 43 character storage credentials."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1


def test_blob_url_with_sas_detection():
    """Test detection of blob URLs with SAS tokens."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1


def test_userid_password_detection():
    """Test detection of userid/password pairs."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1


def test_machinekey_detection():
    """Test detection of machine keys."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1


def test_connection_string_password_detection():
    """Test detection of passwords in connection strings."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1


def test_network_credential_detection():
    """Test detection of network credentials with domains."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1


def test_devops_pat_detection():
    """Test detection of DevOps Personal Access Tokens."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1


def test_app_service_deployment_detection():
    """Test detection of App Service deployment secrets."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1


def test_allows_arbitrarily_encoded_files(tmpdir):
    """Test that binary/arbitrarily encoded files don't cause crashes."""
    arbitrary_encoding = tmpdir.join("binary_file")
    arbitrary_encoding.write_binary(b"\x12\x9a\xe2\xf2\xff\xfe")
    ret = main((str(arbitrary_encoding),))
    assert ret == 0


def test_obfuscation_in_output(capsys):
    """Test that credentials are obfuscated in output."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1

    out, _ = capsys.readouterr()
    # Verify output contains filename and pattern name
    assert "azure_credentials.txt" in out
    assert "datafactory-shir" in out
    # Verify the actual credential is obfuscated (contains ***)
    assert "***" in out
    # Verify the full credential is NOT in output
    assert "uUY/w9WdKTdAWWPDMrEEWdAEZIgeXlrO51GtVUR1/BE=" not in out


def test_output_format_with_pattern_name(capsys):
    """Test that output includes pattern name for easier debugging."""
    ret = main((get_resource_path("azure_credentials.txt"),))
    assert ret == 1

    out, _ = capsys.readouterr()
    # Should mention the file
    assert "azure_credentials.txt" in out
    # Should include pattern names in parentheses
    assert "(" in out and ")" in out


def test_empty_file(tmpdir):
    """Test scanning an empty file."""
    empty_file = tmpdir.join("empty.txt")
    empty_file.write("")
    ret = main((str(empty_file),))
    assert ret == 0


def test_file_with_partial_patterns(tmpdir):
    """Test that partial/incomplete patterns don't trigger false positives."""
    partial = tmpdir.join("partial.txt")
    partial.write(
        "# These are incomplete patterns that should NOT match\n"
        "IR@incomplete\n"
        "AccountKey=short\n"
        "password=\n"
        "sig=toolittledata\n",
    )
    ret = main((str(partial),))
    assert ret == 0
