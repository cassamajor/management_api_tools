# © 2021 Ionic Security Inc. By using this code, I agree to the Terms & Conditions (https://dev.ionic.com/use).

""" Machina Authentication. """

from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import base64
import hmac

import requests
from requests.auth import AuthBase


@dataclass
class MachinaLogin:
    """ Authenticate to the Machina API. """
    instance_id: str
    instance_url: str = field(init=False, default=None)
    api_session: requests.Session = field(init=False, repr=False, default_factory=requests.Session)

    def __post_init__(self) -> None:
        self.instance_url = f'https://api.ionic.com/v2/{self.instance_id}'

    def basic_authentication(self, username: str, password: str) -> None:
        """ Use Basic Authentication to authenticate with the Machina API. """
        self.api_session.auth = (username, password)

    def bearer_authentication(self, token: str) -> None:
        """ Use Bearer Authentication to authenticate with the Machina API. """
        self.api_session.headers.update({'Authorization': f'Bearer {token}'})

    def hmac_authentication(self, identity: str, secret: str) -> None:
        """ Use HMAC Authentication to authenticate with the Machina API. """
        self.api_session.auth = HmacAuth(identity=identity, secret=secret)


@dataclass
class HmacAuth(AuthBase):
    """ Attaches HMAC Authentication to a given Request object. """
    identity: str
    secret: str

    def create_signature(self, string_to_sign: str) -> str:
        """ Construct a valid HMAC signature. """
        begin_signature = hmac.new(key=base64.b64decode(self.secret),
                                   msg=string_to_sign.encode(),
                                   digestmod=hashlib.sha1)
        end_signature = begin_signature.digest()
        final_signature = base64.b64encode(end_signature).decode()
        return final_signature

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        method = request.method
        content_md5_header = request.headers.get('Content-MD5', '')
        content_type_header = request.headers.get('Content-Type', 'application/json; charset=UTF-8')
        date_header = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
        path_url, *_ = request.path_url.split('?')  # Remove query parameters, else HMAC signature does not match.

        string_to_sign = f'{method}\n{content_md5_header}\n{content_type_header}\n{date_header}\n{path_url}'
        signature = self.create_signature(string_to_sign=string_to_sign)
        authorization_header = f'IONIC {self.identity}:{signature}'

        request.headers['Date'] = date_header
        request.headers['Content-MD5'] = content_md5_header
        request.headers['Content-Type'] = content_type_header
        request.headers['Authorization'] = authorization_header

        return request
