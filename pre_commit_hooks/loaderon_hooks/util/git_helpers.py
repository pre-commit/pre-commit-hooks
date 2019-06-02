# -*- coding: utf-8 -*-
import subprocess


def get_current_branch_name():
    output = subprocess.check_output(['git', 'symbolic-ref', 'HEAD'])
    output = output.splitlines()
    head_branches = output[0]
    return head_branches.strip().split('/')[-1]
