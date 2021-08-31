#!/usr/bin/env python3
# © 2021 Ionic Security Inc. By using this code, I agree to the Terms & Conditions (https://dev.ionic.com/use).

""" Sample usage to backup data policies. """


from collections.abc import Generator
from pathlib import Path
import logging
import json

from management_api_tools import Machina


def gather_data_policies(api: Machina) -> Generator:
    """ Gather existing Data Policies. """
    endpoint = api.list_policies()
    policies_list = endpoint.json()['Resources'] if endpoint.ok else exit(f'API call failed: {endpoint.reason}')

    fields = ('status', 'enabled', 'policyId', 'description', 'ruleCombiningAlgId', 'rules')
    policies_generator = ({field: policy[field] for field in fields}
                          for policy in policies_list)

    return policies_generator


def save_data_policies(policy: dict, backup_directory: Path) -> None:
    """ Save a Data Policy to disk. """
    backup_directory.mkdir(exist_ok=True)

    raw_filename = policy['policyId'].replace(' ', '_')
    filename = f'{raw_filename}.json'

    # Construct new Path object rather than use the `joinpath` method because user input is not sanitized.
    backup_location = Path(f'{backup_directory}/{filename}')
    output = json.dumps(obj=policy, indent=4)

    backup_location.write_text(output)
    logging.info(f'Wrote Data Policy to {backup_location}')


def main() -> None:
    instance_id = ''
    username = ''
    password = ''

    api = Machina(instance_id=instance_id)
    api.basic_authentication(username=username, password=password)
    backup_directory = Path.home().joinpath('machina_data_policies')  # No leading /

    for data_policy in gather_data_policies(api=api):
        save_data_policies(policy=data_policy, backup_directory=backup_directory)


if __name__ == '__main__':
    main()
