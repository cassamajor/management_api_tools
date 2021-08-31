# © 2021 Ionic Security Inc. By using this code, I agree to the Terms & Conditions (https://dev.ionic.com/use).

""" Python SDK for the Machina Data Policies API. """

from dataclasses import dataclass
from typing import Any

import requests

from management_api_tools import MachinaLogin


@dataclass
class DataPolicies(MachinaLogin):
    """
    Data policies allow developers to create rules for how data can be accessed.
    The /policies resource is used to administer policies for a tenant.
    Administrators can perform list, fetch, create, update, and delete actions on policies using these API endpoints.
    Developer Documentation: https://dev.ionic.com/api/policies
    """
    def list_policies(self, **kwargs: Any) -> requests.Response:
        """
        Returns a list of information about data policies that match the specified query parameters.
        Developer Documentation: https://dev.ionic.com/api/policies/list-policies
        """
        api_endpoint_url = f'{self.instance_url}/policies'

        response = self.api_session.get(url=api_endpoint_url, params=kwargs)
        return response

    def fetch_policy(self, policy_identifier: str) -> requests.Response:
        """
        Returns the specified data policy.
        Developer Documentation: https://dev.ionic.com/api/policies/fetch-policy
        """
        api_endpoint_url = f'{self.instance_url}/policies/{policy_identifier}'

        response = self.api_session.get(url=api_endpoint_url)
        return response

    def create_policy(self, policy_document: str) -> requests.Response:
        """
        Creates a new data policy.
        Developer Documentation: https://dev.ionic.com/api/policies/create-policy
        """
        api_endpoint_url = f'{self.instance_url}/policies/'

        response = self.api_session.post(url=api_endpoint_url, data=policy_document)
        return response

    def update_policy(self, policy_identifier: str, policy_document: str) -> requests.Response:
        """
        Update an existing data policy.
        Developer Documentation: https://dev.ionic.com/api/policies/update-policy
        """
        api_endpoint_url = f'{self.instance_url}/policies/{policy_identifier}'

        response = self.api_session.put(url=api_endpoint_url, data=policy_document)
        return response

    def create_update_multiple_policies(self, policy_document: str, merge=False) -> requests.Response:
        """
        Creates or updates one or more data policies.
        Developer Documentation: https://dev.ionic.com/api/policies/create-or-update-multiple-policies
        """
        api_endpoint_url = f'{self.instance_url}/policies'

        response = self.api_session.post(url=api_endpoint_url, data=policy_document, params={'merge': merge})
        return response

    def delete_policy(self, policy_identifier: str) -> requests.Response:
        """
        Deletes the specified data policy.
        Developer Documentation: https://dev.ionic.com/api/policies/delete-policy
        """
        api_endpoint_url = f'{self.instance_url}/policies/{policy_identifier}'

        response = self.api_session.delete(url=api_endpoint_url)
        return response