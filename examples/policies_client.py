#!/usr/bin/env python3
# © 2021 Ionic Security Inc. By using this code, I agree to the Terms & Conditions (https://dev.ionic.com/use).

""" Sample usage of the Data Policy API. """

from dataclasses import dataclass
from pathlib import Path
import json

from unofficial_sdk import Machina


@dataclass
class Policy:
    """ Data container for fetched policies. """
    id: str
    policyId: str
    description: str


#######################
# Variables to modify #
#######################
INSTANCE_ID: str = 'ABC123'
USERNAME: str = 'ionic@security.com'
PASSWORD: str = 'ciphertext'
SECRET_TOKEN: str = 'bearer_token='
HMAC_IDENTITY: str = 'identity'
HMAC_SECRET: str = 'secret='
POLICY_DATA: Policy = Policy(id='123ABC', policyId='pid', description='description')


def list_policies_example():
    """ List policy example. """
    api = Machina(instance_id=INSTANCE_ID)
    api.basic_authentication(username=USERNAME, password=PASSWORD)

    return api.list_policies()


def fetch_policy_example():
    """ Fetch policy example. """
    api = Machina(instance_id=INSTANCE_ID)
    api.bearer_authentication(token=SECRET_TOKEN)
    policies_list = api.list_policies().json()['Resources']
    policies_generator = (Policy(id=policy['id'], policyId=policy['policyId'], description=policy['description'])
                          for policy in policies_list)

    for policy in policies_generator:
        yield api.fetch_policy(policy_identifier=policy.id)


def create_policy_example():
    """ Create policy example. """
    document = Path.home().joinpath('Downloads/data-policy.json')
    policy_document = document.read_text()

    api = Machina(instance_id=INSTANCE_ID)
    api.hmac_authentication(identity=HMAC_IDENTITY, secret=HMAC_SECRET)
    return api.create_policy(policy_document=policy_document)


def update_policy_example():
    """ Update policy example. """
    document = Path.cwd().joinpath('policy_documents/update-allow-all-by-data-creator.json')
    policy_document = document.read_text(encoding='utf-8-sig')

    api = Machina(instance_id=INSTANCE_ID)
    api.hmac_authentication(identity=HMAC_IDENTITY, secret=HMAC_SECRET)
    return api.update_policy(policy_identifier=POLICY_DATA.id, policy_document=policy_document)


def create_update_multiple_policies_example():
    """ Create or update multiple policies example. """
    document = Path.cwd().joinpath('policy_documents/merge-allow-all-by-data-creator.json')
    policy_document = document.read_text(encoding='utf-8-sig')

    api = Machina(instance_id=INSTANCE_ID)
    api.hmac_authentication(identity=HMAC_IDENTITY, secret=HMAC_SECRET)
    return api.create_update_multiple_policies(policy_document=policy_document, merge=True)


def delete_policy_example():
    """ Delete policy example. """
    api = Machina(instance_id=INSTANCE_ID)
    api.hmac_authentication(identity=HMAC_IDENTITY, secret=HMAC_SECRET)
    return api.delete_policy(policy_identifier=POLICY_DATA.id)


if __name__ == '__main__':
    pass
    # list_policies = list_policies_example()
    # list_policies_json = list_policies.json()
    # list_policies_pretty = json.dumps(obj=list_policies_json, indent=4)
    # print(list_policies_pretty)

    # fetch_policy = fetch_policy_example()
    # fetch_policy_json = [policy.json() for policy in fetch_policy]
    # fetch_policy_pretty = json.dumps(obj=fetch_policy_json, indent=4)
    # print(fetch_policy_pretty)

    # create_policy = create_policy_example()
    # create_policy_json = create_policy.json()
    # create_policy_pretty = json.dumps(obj=create_policy_json, indent=4)
    # print(create_policy_pretty)

    # update_policy = update_policy_example()
    # update_policy_json = update_policy.json()
    # update_policy_pretty = json.dumps(obj=update_policy_json, indent=4)
    # print(update_policy_pretty)

    # create_update_multiple_policies = create_update_multiple_policies_example()
    # create_update_multiple_policies_json = create_update_multiple_policies.json()
    # create_update_multiple_policies_pretty = json.dumps(obj=create_update_multiple_policies_json, indent=4)
    # print(create_update_multiple_policies_pretty)

    # delete_policy = delete_policy_example()
    # print(delete_policy)
