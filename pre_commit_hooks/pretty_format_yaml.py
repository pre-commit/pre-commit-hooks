from __future__ import print_function

import argparse
import sys

import yaml


def _get_pretty_format(content, **kwargs):
    return yaml.safe_dump(yaml.safe_load(content), **kwargs)


def _autofix(filename, new_contents):
    print("Fixing file {0}".format(filename))
    with open(filename, 'w') as f:
        f.write(new_contents)


def filter_argument(accepted_values):
    def _validate(s):
        try:
            return {str(v): v for v in accepted_values}[s]
        except:
            raise argparse.ArgumentTypeError('Accepted values are: {}'.format(accepted_values))
    return _validate


def none_or_boolean_argument(s):
    return filter_argument([None, True, False])(s)


def pretty_format_yaml(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--autofix',
        action='store_true',
        dest='autofix',
        help='Automatically fixes encountered not-pretty-formatted files',
    )

    parser.add_argument(
        '--default_style',
        help='PyYAML dump parameter. More info on http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper'
    )
    parser.add_argument(
        '--default_flow_style', type=none_or_boolean_argument,
        help='PyYAML dump parameter. More info on http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper'
    )
    parser.add_argument(
        '--canonical', type=none_or_boolean_argument,
        help='PyYAML dump parameter. More info on http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper'
    )
    parser.add_argument(
        '--indent', type=int,
        help='PyYAML dump parameter. More info on http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper'
    )
    parser.add_argument(
        '--width', type=int,
        help='PyYAML dump parameter. More info on http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper'
    )
    parser.add_argument(
        '--allow_unicode', type=none_or_boolean_argument,
        help='PyYAML dump parameter. More info on http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper'
    )
    parser.add_argument(
        '--line_break', type=none_or_boolean_argument,
        help='PyYAML dump parameter. More info on http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper'
    )
    parser.add_argument(
        '--encoding',
        help='PyYAML dump parameter. More info on http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper'
    )
    parser.add_argument(
        '--explicit_start', type=none_or_boolean_argument,
        help='PyYAML dump parameter. More info on http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper'
    )
    parser.add_argument(
        '--explicit_end', type=none_or_boolean_argument,
        help='PyYAML dump parameter. More info on http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper'
    )
    parser.add_argument(
        '--version',
        help='PyYAML dump parameter. More info on http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper'
    )
    parser.add_argument(
        '--tags',
        help='PyYAML dump parameter. More info on http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper'
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    pyyaml_kwargs = {
        key: value
        for key, value in args._get_kwargs()
        if key != 'autofix' and key != 'filenames'
    }

    status = 0

    for yaml_file in args.filenames:
        with open(yaml_file) as f:
            contents = f.read()

        try:
            pretty_contents = _get_pretty_format(contents, **pyyaml_kwargs)

            if contents != pretty_contents:
                print("File {0} is not pretty-formatted".format(yaml_file))

                if args.autofix:
                    _autofix(yaml_file, pretty_contents)

                status = 1

        except yaml.YAMLError:
            print(
                "Input File {0} is not a valid YAML, consider using check-yaml"
                .format(yaml_file)
            )
            return 1

    return status


if __name__ == '__main__':
    sys.exit(pretty_format_yaml(sys.argv[1:]))
