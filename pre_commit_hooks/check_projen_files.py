from __future__ import annotations

import subprocess
import sys

def main():
    projen_process = subprocess.run('yarn projen', shell=True)
    
    if projen_process.returncode != 0:
        print(f'Error: "yarn projen" failed with exit status {projen_process.returncode}')
        sys.exit(projen_process.returncode)

    git_status = subprocess.run('git diff', capture_output=True, shell=True, text=True)
    if git_status.stdout.strip():
        print("Uncommitted changes found:")
        print(git_status.stdout)
        print('Have you forgotten to run "yarn projen" and commit changes?')
        sys.exit(1)

if __name__ == '__main__':
    raise SystemExit(main())