import argparse
import json
from typing import Optional
from typing import Sequence
from pathlib import Path


def _check_duplicate_entry(json_entries, pkeys):
    """ Check duplicate entry based on pkey criteria.

    :param json_entries: List of json entries
    :param pkeys: List of Primary keys
    :return: list of duplicated entry pkey value tuples
    """
    unique_entries = set()
    duplicate_entries = set()
    for entry in json_entries:
        pkey_value_tuple = tuple(entry[pkey] for pkey in pkeys)
        if pkey_value_tuple not in unique_entries:
            unique_entries.add(pkey_value_tuple)
        else:
            duplicate_entries.add(pkey_value_tuple)
    return duplicate_entries, len(duplicate_entries)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', type=str,
                        help='Names of the JSON files to check duplicate entries'
                        )
    table_uuid_mapping = {
        'action': ['uuid'],
        'env_property_group': ['uuid'],
        'environment': ['uuid'],
        'environment_property': ['code'],
        'report_summary': ['uuid'],
        'runner': ['uuid'],
        'scenario': ['uuid'],
        'sla': ['uuid'],
        'sla_scenario_association': ['sla', 'scenario'],
        'tag': ['uuid'],
        'tag_action_association': ['tag_uuid', 'action_uuid'],
        'tag_case_association': ['test_case_uuid', 'tag_uuid'],
        'teams': ['uuid'],
        'test_case': ['uuid'],
        'test_suit': ['uuid'],
        'test_supported_version': ['test_case_uuid', 'version'],
        'testcase_workload_association': ['uuid'],
        'user': ['uuid'],
        'user_tokens': ['user_token'],
        'workflow_task': ['workflow_id'],
        'context': ['uuid'],
        'test_sla_association': ['test_case', 'sla'],
        'teams_association': ['user_uuid', 'team_uuid'],
        'teams_resource_permission': ['team_uuid', 'resource_name'],
        'label': ['uuid'],
    }

    args = vars(parser.parse_args(argv))
    filenames = args['filenames']
    flag = False

    for i in range(len(filenames)):
        json_file = filenames[i]
        file_name = Path(filenames[i]).stem
        pkeys = table_uuid_mapping[file_name]
        with open(json_file, encoding='UTF-8') as f:
            json_entries = json.load(f)
        duplicate_entries, status = _check_duplicate_entry(json_entries, pkeys)

        if status:
            print(f"Duplicate entries found - {duplicate_entries} in file "
                  f"{json_file}")
            flag = True

    return flag


if __name__ == "__main__":
    exit(main())
