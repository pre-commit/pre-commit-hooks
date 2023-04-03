import argparse
import json
from typing import Optional
from typing import Sequence
from pathlib import Path

def _check_duplicate_entry(json_contents, key):
    json_dict = {}
    duplicate_uuids = set()
    for row in json_contents:
        if row[key] not in json_dict:
            json_dict[row[key]] = row
        else:
            duplicate_uuids.add(row[key])
    return duplicate_uuids, len(duplicate_uuids)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', type=str,
                        help='Names of the JSON files to check duplicate entries'
                        )
    table_uuid_mapping = {
        'action': 'uuid', 'env_property_group': 'uuid',
        'environment': 'uuid', 'environment_property': 'code',
        'report_summary': 'uuid',
        'runner': 'uuid', 'scenario': 'uuid',
        'sla': 'uuid', 'sla_scenario_association': 'sla', 'tag': 'uuid',
        'tag_action_association': 'tag_uuid',
        'tag_case_association': 'test_case_uuid',
        'teams': 'uuid',
        'test_case': 'uuid',
        'test_suit': 'uuid', 'test_supported_version': 'test_case_uuid',
        'testcase_workload_association': 'uuid', 'user': 'uuid',
        'user_tokens': 'user_token', 'workflow_task': 'workflow_id'
    }

    args = vars(parser.parse_args(argv))
    filenames = args['filenames']
    flag = False

    for i in range(len(filenames)):
        json_file = filenames[i]
        file_name = Path(filenames[i]).stem
        key = table_uuid_mapping[file_name]
        with open(json_file, encoding='UTF-8') as f:
            contents = json.load(f)
        duplicate_uuids, status = _check_duplicate_entry(contents, key)

        if status:
            print(f"Duplicate UUIDs found - {duplicate_uuids} in file "
                  f"{json_file}")
            flag = True

    return flag


if __name__ == "__main__":
    exit(main())
