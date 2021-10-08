from pre_commit_hooks.check_number_of_lines_count import main


def test_number_of_lines_count_bad(fs):
    max_lines = 42

    filename = 'lines_count_bad'
    line_contents = [
        f'I am the {line_number+1}. line!'
        for line_number in range(max_lines + 1)
    ]
    fs.create_file(filename, contents='\n'.join(line_contents))

    ret = main([str(filename), f'--max-lines={max_lines}'])
    assert ret == 1


def test_number_of_lines_count_good(fs):
    max_lines = 42

    filename = 'lines_count_good'
    line_contents = [
        f'I am the {line_number+1}. line!'
        for line_number in range(max_lines)
    ]
    fs.create_file(filename, contents='\n'.join(line_contents))

    ret = main([str(filename), f'--max-lines={max_lines}'])
    assert ret == 0
