__copyright__ = "\u00A9 2021 Ionic Security Inc. By using this code, I agree to the Terms & Conditions (https://dev.ionic.com/use)."

from management_api_tools.utils.auth import MachinaLogin
from management_api_tools.api import Metrics, DataPolicies


class Machina(Metrics, DataPolicies):
    pass
