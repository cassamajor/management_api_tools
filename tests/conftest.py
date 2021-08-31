# © 2021 Ionic Security Inc. By using this code, I agree to the Terms & Conditions (https://dev.ionic.com/use).

""" Test the Machina implementation. """
from pathlib import Path

import pytest

from management_api_tools import Machina
from parserconfig import ParserConfig

CONFIGURATION_FILE = Path.home().joinpath('.machina/settings.ini')

BASIC, BEARER, HMAC = 'basic', 'bearer', 'hmac'

AUTHENTICATION = [
    pytest.param(BASIC, marks=pytest.mark.basic_authentication, id='basic_auth'),
    pytest.param(BEARER, marks=pytest.mark.bearer_authentication, id='bearer_auth'),
    pytest.param(HMAC, marks=pytest.mark.hmac_authentication, id='hmac_auth'),
]


def load_credentials(*options, section: str, configuration_file: Path = CONFIGURATION_FILE) -> dict:
    """ Read the configuration file with defined settings. Skip a given test if the section or option does not exist."""
    settings = ParserConfig(configuration_file=configuration_file)

    if not settings.configuration_file_parser.has_section(section):
        pytest.skip(msg=f'Section {section} not in {configuration_file.as_posix()}')

    for option in options:
        if not settings.configuration_file_parser.has_option(section=section, option=option):
            pytest.skip(msg=f'Section {section} does not have option {option} in {configuration_file.as_posix()}')

    return settings.credentials(*options, section=section)


def read_document(document_path: str) -> str:
    """ Read text from the specified document. """
    try:
        # expanduser() will expand ~/, while resolve() will make symlinks absolute.
        document = Path(document_path).expanduser().resolve()
        return document.read_text(encoding='utf-8-sig')
    except Exception as error:
        pytest.skip(msg=f'{error}')


def init_machina(section) -> Machina:
    """ Return an authenticated Machina object for each environment. """
    instance_id = load_credentials('instance_id', section=section)
    machina = Machina(**instance_id)

    if section == BASIC:
        credentials = load_credentials('username', 'password', section=section)
        machina.basic_authentication(**credentials)

    if section == BEARER:
        credentials = load_credentials('token', section=section)
        machina.bearer_authentication(**credentials)

    if section == HMAC:
        credentials = load_credentials('identity', 'secret', section=section)
        machina.hmac_authentication(**credentials)

    return machina


def init_policy_identifier(machina: Machina, section: str) -> str:
    """ Create a data policy to ensure the desired state exists, and use the policy identifier for subsequent tests. """
    # GIVEN a policy document
    document_path, *_ = load_credentials('create_policy', section=section).values()
    policy_document = read_document(document_path=document_path)

    # WHEN I make a request to an API endpoint
    response = machina.create_policy(policy_document=policy_document)

    # THEN the response should include a policy identifier
    return response.json()['id']


def data_policy_resources(section: str) -> dict:
    """ Converge resources required for completing tests that involve data policies. """
    machina = init_machina(section=section)
    policy_identifier = init_policy_identifier(machina=machina, section=section)

    return dict(Machina=machina, policy_identifier=policy_identifier, section=section)


def delete_data_policy(machina, policy_identifier):
    """ Delete a data policy. """
    # GIVEN an authenticated Machina instance and a policy_identifier

    # WHEN I make a request to an API endpoint
    machina.delete_policy(policy_identifier=policy_identifier)

    # THEN the policy should be deleted


@pytest.fixture(params=AUTHENTICATION, name='Machina')
def authenticated_machina_instance(request) -> Machina:
    """ Return an authenticated Machina object for each authentication method. """
    return init_machina(section=request.param)


@pytest.fixture(params=AUTHENTICATION)
def machina_resources(request) -> dict:
    """ This fixture provides a policy identifier to tests, then deletes the data policy upon completion. """
    credentials = data_policy_resources(section=request.param)
    machina, policy_identifier, section = credentials.values()

    yield credentials
    delete_data_policy(machina=machina, policy_identifier=policy_identifier)
