import os
import sys


def get_sample_file_path(file_name):
    current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    testing_files_folder_path = current_path + '/testing_files/'
    return testing_files_folder_path + file_name


def perform_test_on_file_expecting_result(file_name, test_function, expected_result=0):
    sample_file_path = get_sample_file_path(file_name)
    sys.argv.append(sample_file_path)

    result = test_function(sys.argv)

    assert result == expected_result
