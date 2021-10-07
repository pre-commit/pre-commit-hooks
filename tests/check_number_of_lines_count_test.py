from pre_commit_hooks.check_number_of_lines_count import main


def test_number_of_lines_count_bad(tmpdir):
    max_lines = 30
    line_contents = []
    filename = tmpdir.join('lines_count_bad')

    for line_number in range(max_lines + 1):
        line_contents.append(f'I am the {line_number+1}. line!')

    with open(filename, 'w') as file:
        file.write('\n'.join(line_contents))

    ret = main([str(filename), f'--max-lines={max_lines}'])
    assert ret == 1


def test_number_of_lines_count_good(tmpdir):
    max_lines = 30
    line_contents = []
    filename = tmpdir.join('lines_count_good')

    for line_number in range(max_lines):
        line_contents.append(f'I am the {line_number+1}. line!')

    with open(filename, 'w') as file:
        file.write('\n'.join(line_contents))

    ret = main([str(filename), f'--max-lines={max_lines}'])
    assert ret == 0
