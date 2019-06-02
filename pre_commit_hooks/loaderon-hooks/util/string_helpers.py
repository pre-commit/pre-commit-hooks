# -*- coding: utf-8 -*-
import re


def matches_any_regexp(string, regexp_list):
    """Checks if string matches any of regexp in regexp_list."""
    for regexp in regexp_list:
        pattern = re.compile(regexp)
        if pattern.match(string):
            return True
    return False
