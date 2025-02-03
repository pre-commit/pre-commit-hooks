#!/usr/bin/env python3
"""
This script checks files for potential Web3 private keys.
"""

import argparse
import os
import re
import sys
from typing import Sequence

from eth_account import Account
from eth_utils import decode_hex

# Regular expression to match Ethereum private keys
KEY_PATTERN = re.compile(r"\b(0x)?[a-fA-F0-9]{64}\b")
IGNORE_COMMENT = "# web3-private-key-ok"


def is_private_key_valid(private_key_hex: str) -> bool:
    try:
        # Remove hex prefix if present
        if private_key_hex.startswith("0x"):
            private_key_hex = private_key_hex[2:]

        # Decode the hex string to bytes
        private_key_bytes = decode_hex(private_key_hex)

        # Attempt to create an account object
        Account.from_key(private_key_bytes)

        return True

    except Exception:
        return False


def scan_file(file_path: str) -> bool:
    """
    Scans a file for potential Web3 private keys.
    """
    detected = False
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for idx, line in enumerate(f):
                match = KEY_PATTERN.search(line)
                if match and IGNORE_COMMENT not in line:
                    private_key_hex = match.group(0)
                    if is_private_key_valid(private_key_hex):
                        print(
                            f"Error: Valid Web3 private key detected in {file_path}:{idx + 1}"
                        )
                        detected = True
    except Exception as e:
        print(f"Warning: Error reading file {file_path}: {e}")
    return detected


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check")
    args = parser.parse_args(argv)

    files_with_keys = []
    for file_path in args.filenames:
        if not os.path.isfile(file_path):
            continue

        if scan_file(file_path):
            files_with_keys.append(file_path)

    if files_with_keys:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
