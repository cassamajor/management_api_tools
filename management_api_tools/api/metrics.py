# © 2021 Ionic Security Inc. By using this code, I agree to the Terms & Conditions (https://dev.ionic.com/use).

""" Python SDK for the Machina Metrics API. """

from dataclasses import dataclass
from typing import Any

import requests

from management_api_tools import MachinaLogin


@dataclass
class Metrics(MachinaLogin):
    """
    The metrics API allows developers to retrieve metrics recorded for various request types.
    Metrics are available as a series of points over time, with each metric point describing activity within a fixed
    size period.
    Developer Documentation: https://dev.ionic.com/api/metrics/metrics-api
    """
    def metrics(self, **kwargs: Any) -> requests.Response:
        """
        The metrics API allows developers to retrieve metrics recorded for various request types.
        Metrics are available as a series of points over time, with each metric point describing activity within a fixed
        size period.
        Developer Documentation: https://dev.ionic.com/api/metrics/metrics-api
        """
        api_endpoint_url = f'{self.instance_url}/metrics'

        response = self.api_session.get(url=api_endpoint_url, params=kwargs)
        return response
