from __future__ import annotations

import unittest
from unittest.mock import mock_open
from unittest.mock import patch

from pre_commit_hooks.detect_gcp_credentials import detect_gcp_credentials_in_file


class TestDetect(unittest.TestCase):

    @patch('builtins.open', mock_open(read_data="Some content with GCP credentials: 'AIzaSyCzQ2rBq4dd8uf4Gh9J7G1IiCvC5q8oCvk'"))
    def test_detect_gcp_api_key(self):
        result = detect_gcp_credentials_in_file('')
        self.assertIn('AIzaSyCzQ2rBq4dd8uf4Gh9J7G1IiCvC5q8oCvk', result)

    @patch('builtins.open', mock_open(read_data="Some content with GCP credentials: '-----BEGIN PRIVATE KEY-----\nAbCdEf1234567890\n-----END PRIVATE KEY-----'"))
    def test_detect_gcp_service_account_key(self):
        result = detect_gcp_credentials_in_file('')
        self.assertIn('-----BEGIN PRIVATE KEY-----\nAbCdEf1234567890\n-----END PRIVATE KEY-----', result)


if __name__ == '__main__':
    unittest.main()
