# -*- coding: utf-8 -*-
import os
import re


def read_file(file_path, only_first_line=False):
    opened_file = open(file_path)
    if only_first_line:
        lines = opened_file.readline()
    else:
        lines = opened_file.readlines()
    opened_file.close()
    return lines


def read_file_line(file_path):
    return read_file(file_path, True)


def read_file_lines(file_path):
    return read_file(file_path)


def find_file_starting_from_reference_file_directory(reference_file, file_to_find):
    """Attempts to find file_to_find by navigating through directories from reference_file parent directory."""
    file_path = os.path.realpath(reference_file)
    folder_path = os.path.dirname(file_path)
    for root, unused_dirs, files in os.walk(folder_path):
        if file_to_find in files:
            return os.path.join(root, file_to_find)
    return None


def get_indexes_of_lines_per_regex(file_lines, regex):
    regex_pattern = re.compile(regex)
    indexes_of_lines_defining_regex = []
    for index, line in enumerate(file_lines):
        if regex_pattern.match(line):
            indexes_of_lines_defining_regex.append(index)
    return indexes_of_lines_defining_regex


def get_bunches_of_lines_dividing_by_regex(file_lines, regex):
    lines = []
    indexes_of_lines_per_regex = get_indexes_of_lines_per_regex(file_lines, regex)
    for index, index_of_lines in enumerate(indexes_of_lines_per_regex):
        try:
            next_regex_index = indexes_of_lines_per_regex[index + 1]
            current_regex_lines = file_lines[index_of_lines:next_regex_index]
        except IndexError:
            current_regex_lines = file_lines[index_of_lines:]
        lines.append(current_regex_lines)
    return lines


def split_by_regexp(filename, regex):
    file_lines = read_file_lines(filename)
    return get_bunches_of_lines_dividing_by_regex(file_lines, regex)
