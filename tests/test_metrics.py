# © 2021 Ionic Security Inc. By using this code, I agree to the Terms & Conditions (https://dev.ionic.com/use).

""" Test the Metrics implementation. """

from datetime import datetime, timezone, timedelta


def test_metrics(Machina):
    """ Query the total users. """
    # GIVEN an authenticated Machina instance

    # WHEN I specify valid parameters
    end = datetime.now(timezone.utc)
    start = end + timedelta(days=-1)
    metric = {'start': f'{start.strftime("%Y%m%d-00:00")}', 'end': 'now', 'bucket': '1d', 'metric': 'total-users'}

    # WHEN I make a request to an API endpoint
    api_endpoint = Machina.metrics(**metric)

    # THEN the status code should be 200
    assert api_endpoint.status_code == 200, f'Failed: {api_endpoint.json()}'
