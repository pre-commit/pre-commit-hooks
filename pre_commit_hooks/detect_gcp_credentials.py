"""Check for some harcoded gcp credentials."""
from __future__ import annotations

import os
import sys
import re


def detect_gcp_credentials_in_file(file_path):
    """
    Detect potential Google Cloud Platform (GCP) credentials in a Python file.

    Args:
    - file_path (str): The path to the Python file to scan.

    Returns:
    - list: A list of potential GCP credentials found in the file.
    """
    with open(file_path, "r") as file:
        code = file.read()

    # Regular expression patterns for common GCP credential formats
    credential_patterns = [
        r"'(AIza[0-9A-Za-z_\-]{35})'",  # GCP API Key
        r"'(-----BEGIN PRIVATE KEY-----[A-Za-z0-9+\/=\n]+-----END PRIVATE KEY-----)'"  # GCP Service Account Key
        # Add more patterns for other types of GCP credentials as needed
    ]

    credentials = []

    # Search for patterns in the code
    for pattern in credential_patterns:
        matches = re.findall(pattern, code)
        credentials.extend(matches)

    return credentials

def scan_directory(directory):
    """
    Scan a directory and its subdirectories for Python files and check for potential GCP credentials.

    Args:
    - directory (str): The path to the directory to scan.
    """
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            gcp_credentials = detect_gcp_credentials_in_file(file_path)
            if gcp_credentials:
                print(f"🔴 Potential GCP credentials found in: {file_path}")
                print("Credentials:")
                for credential in gcp_credentials:
                    print(credential)

def main():
    file_paths = sys.stdin.read().strip().split('\n')

    # Process each file
    for file_path in file_paths:
        credentials = detect_gcp_credentials_in_file(file_path)

        # Check if any credentials were found
        if credentials:
            print("🔴 Potential GCP credentials found:")
            for credential in credentials:
                print(credential)
            print("Please remove these credentials before committing.")
            return 1  # Abort the commit with a non-zero exit code
        return 0

# Example usage
if __name__ == "__main__":
    raise SystemExit(main())
