# © 2021 Ionic Security Inc. By using this code, I agree to the Terms & Conditions (https://dev.ionic.com/use).

""" Test the DataPolicies implementation. """

from conftest import load_credentials, read_document


def test_list_policies(Machina):
    """ List policies test. """
    # GIVEN an authenticated Machina instance

    # WHEN I make a request to an API endpoint
    response = Machina.list_policies()

    # THEN the status code should be 200
    assert response.status_code == 200, f'Failed: {response.json()}'


def test_fetch_policy(machina_resources):
    """ Fetch policy test. """
    # GIVEN an authenticated Machina instance and a policy_identifier
    Machina, policy_identifier, section = machina_resources.values()

    # WHEN I make a request to an API endpoint
    response = Machina.fetch_policy(policy_identifier=policy_identifier)

    # THEN the status code should be 200
    assert response.status_code == 200, f'Failed: {response.json()["detail"]["message"]}'


def test_create_policy(machina_resources):
    """ Create policy test. """
    # GIVEN a policy_identifier
    Machina, policy_identifier, section = machina_resources.values()

    # THEN the policy was successfully created in the fixture
    assert policy_identifier


def test_update_policy(machina_resources):
    """ Update policy test. """
    # GIVEN an authenticated Machina instance, a policy identifier, and a section
    Machina, policy_identifier, section = machina_resources.values()

    # GIVEN a policy document
    document_path, *_ = load_credentials('update_policy', section=section).values()
    policy_document = read_document(document_path=document_path)

    # WHEN I make a request to an API endpoint
    response = Machina.update_policy(policy_identifier=policy_identifier, policy_document=policy_document)

    # THEN the status code should be 200
    assert response.status_code == 200, f'Failed: {response.json()["detail"]["message"]}'


def test_create_update_multiple_policies(machina_resources):
    """ Create or update multiple policies test. """
    # GIVEN an authenticated Machina instance and a section
    Machina, policy_identifier, section = machina_resources.values()

    # GIVEN a policy document
    document_path, *_ = load_credentials('create_policy', section=section).values()
    policy_document = read_document(document_path=document_path)

    # WHEN I make a request to an API endpoint
    response = Machina.create_update_multiple_policies(policy_document=policy_document, merge='replace')

    # THEN the status code should be 200 if updated, 201 if created
    assert response.status_code in (200, 201), f'Failed: {response.json()["detail"]["message"]}'


def test_delete_policy(machina_resources):
    """ Delete policy test. """
    # GIVEN an authenticated Machina instance
    Machina, policy_identifier, section = machina_resources.values()

    # WHEN I make a request to an API endpoint
    response = Machina.delete_policy(policy_identifier=policy_identifier)

    # THEN the status code should be 204
    assert response.status_code == 204, f'Failed: {response.json()["detail"]["message"]}'
