# Management API Tools
This toolkit arose from the need to ensure a consistent state of policies during the 2020 Ionic Hackathon. It has since
evolved and now supports the [Data Policies](https://dev.ionic.com/api/policies) and [Metrics](https://dev.ionic.com/api/metrics) Management API's.

This software is not officially supported by Ionic Security, Inc.

## Features
- Authenticate to Machina using a simple interface for basic, bearer, and HMAC authentication methods.
- List, create, update, backup, and delete data policies programmatically.
- Retrieve metrics activity for various request types.

## Usage
Install management_api_tools (requires Python 3.7+):
```shell
python -m pip install management_api_tools
```

To preserve the current configuration of data policies prior to the execution of a demo,
[backup_policies.py](examples/policies_backup.py) can create a backup of all data policies programmatically.

Alternatively, it is possible to export data policies manually:
1. Login to the Machina Console
1. Go to the Data Policies tab
1. Filter the data policies, if necessary
1. Click Export on the top right
1. Download the file

With the exported policies saved locally, you can use management_api_tools to enforce your desired state:
```python
from pathlib import Path

from management_api_tools import Machina


def first_policy_demo():
    """ Ensure the desired state exists for the first demo. """
    # Modify the path to point to the location of the JSON file.
    document = Path.cwd().joinpath('data-policies.json')
    policy_document = document.read_text(encoding='utf-8-sig')

    api = Machina(instance_id='INSTANCE_ID')
    api.hmac_authentication(identity='HMAC_IDENTITY', secret='HMAC_SECRET')

    # merge='replace' will delete all other data policies that do not exist in the JSON file.
    return api.create_update_multiple_policies(policy_document=policy_document, merge='replace')


def second_policy_demo():
    """ Ensure the desired state exists for the second demo. """
    ...


desired_state = first_policy_demo()
print(desired_state.ok)
```

Additional examples can be found in [policies_client.py](examples/policies_client.py).

## Local Development and Testing
### Development
Development and testing should be done in a virtual environment.
```shell
$ git clone https://github.com/Fauxsys/management_api_tools.git
$ cd management_api_tools
$ python -m venv venv --prompt management_api_tools
$ source venv/bin/activate
(management_api_tools) $ python -m pip install -U pip
```
Install management_api_tools locally.
```shell
(management_api_tools) $ python -m pip install -e ".[test]"
```

### Testing
Review the [design document](tests/README.md) to understand the test runner implementation.

You can test any changes locally with pytest.
```shell
(management_api_tools) $ python -m pytest --cov=management_api_tools
```

You can also test management_api_tools as an installed package.
```shell
(management_api_tools) $ python -m tox
```

### Building a wheel
```shell
(management_api_tools) $ python -m pip install build
(management_api_tools) $ python -m build --wheel
```

There should now be a wheel in the `dist` directory.
```shell
(management_api_tools) $ ls -1 dist
management_api_tools-1.0.0-py3-none-any.whl
```