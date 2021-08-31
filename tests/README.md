# Setup
Follow the "Development" instructions under "Local Development and Testing" in the [project README](../README.md#development). 

# Configuration: File
Modify the `CONFIGURATION_FILE` variable in [conftest.py](conftest.py) to point to where the configuration file exists on the file system.

The content within the configuration file should be similar to this:
```ini
[DEFAULT]
create_policy = examples/policy_documents/create-allow-all-by-data-creator.json
update_policy = examples/policy_documents/update-allow-all-by-data-creator.json
instance_id = REDACTED

[basic]
username = REDACTED
password = REDACTED

[bearer]
token = REDACTED

[hmac]
identity = REDACTED
secret = REDACTED
```

The keys defined in the `[DEFAULT]` section are applicable to all sections.

# Configuration: Pytest
Markers are defined in [pytest.ini](pytest.ini), and applied in [conftest.py](conftest.py). Each authentication method is "marked" which allows it to be executed individually.

```python
AUTHENTICATION = [
    pytest.param(BASIC, marks=pytest.mark.basic_authentication, id='basic_auth'),
    pytest.param(BEARER, marks=pytest.mark.bearer_authentication, id='bearer_auth'),
    pytest.param(HMAC, marks=pytest.mark.hmac_authentication, id='hmac_auth'),
]
```

The first value passed to `pytest.param` references a section defined within the configuration file. This value is then used in each fixture as `request.param`.

Additionally, the `load_credentials` function in [conftest.py](conftest.py) handles situations where an option or section is not defined, and will skip the test as a result.

# Execution: Pytest
Make sure you are in the project root directory. To run all tests for every authentication method, simply run:
```shell
python -m pytest
```

For more granular control:
- The `-m` argument can be used to specify which authentication method(s) to run.
- The `-k` argument can be used to select tests that match the given keyword(s).

These two options can be combined.
```shell
python -m pytest -m basic_authentication
python -m pytest -m "basic_authentication or bearer_authentication"
python -m pytest -m "not hmac_authentication"
python -m pytest -m hmac_authentication -k metrics
```

You can measure code coverage to gauge the effectiveness of tests. The following command can be used to determine which lines of code are executed by tests, and which are not.
```shell
python -m pytest --cov=management_api_tools
```

# Configuration: Tox
Tox is used to execute `pytest`, as configured in [tox.ini](../tox.ini), and supports the same arguments described in the [Execution: Pytest](#execution-pytest) section.
```ini
commands = python -m pytest --cov={envsitepackagesdir}/management_api_tools
```

Running tox will build and install management_api_tools in an isolated environment, which verifies the package structure and validates imports.

Since management_api_tools supports multiple Python versions, tox is also configured to run tests against Python 3.7, 3.8, and 3.9.
```ini
envlist = py3{7,8,9}
```

Please note, it is the responsibility of the developer to ensure these Python versions are installed and configured in the system PATH.

# Execution: Tox
To run tests for all Python versions specified in [tox.ini](../tox.ini), make sure you are in the project root directory, and simply type:
```shell
python -m tox
```

Tox allows Python versions to be specified on the command line as well, using the `-e` flag.
```shell
python -m tox -e py37,py38,py39
```