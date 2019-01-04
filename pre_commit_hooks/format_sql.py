import sys
import click
import os
import sqlparse

options = {"keyword_case": "upper", "comma_first": True}



def reformat(sql_file):
    with open(sql_file, "r") as f:
        original = f.read()
    new = sqlparse.format(original, **options)
    with open(sql_file, "w") as f:
        f.write(new)
    if new == original:
        return 0
    else:
        return 1


@click.command()
@click.option('--directory', required=True)
def main(directory):
    res = 0
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.split('.')[-1] == 'sql':
                res = max(res, reformat(os.path.join(root, f)))
                print(f"reformatted {f}")
    return res


if __name__ == "__main__":
    sys.exit(main())
