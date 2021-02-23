"""Library for Nest API Access"""

import time
import sys
from typing import Mapping, Union
import requests
from settings import Settings
from tokens import Secret
from sensor_lib import BaseSensor
from sensor_lib import CLASS_FOR_SENSOR_TYPE

BASE_GOOGLE_AUTH_URL = "https://www.googleapis.com/oauth2/v4/token"
BASE_NEST_API_URL = "https://smartdevicemanagement.googleapis.com/v1/enterprises"

STRUCTURES_ENDPOINT = "structures"
DEVICES_ENDPOINT = "devices"

API_END_POINTS = {
    STRUCTURES_ENDPOINT: STRUCTURES_ENDPOINT,
    DEVICES_ENDPOINT: DEVICES_ENDPOINT
}

def is_auth_token_valid(token: Secret, jitter: int = 0) -> bool:
    """Returns if the token is still valid (within some jitter window)"""
    if token.token_life == -1:
        return True
    now = int(time.time())
    latest_token_life = token.token_created + token.token_life - jitter
    return latest_token_life > now

class NestAPI:
    def __init__(self, settings: Settings):
        self._settings = settings
    def error_handler(self, resp_json):
        print(resp_json)
    def post(self, url, headers=None, params=None) -> requests.Response:
        #print(url, headers, params)
        #response = SimpleNamespace(status_code=404)
        response = requests.post(url, headers=headers, params=params)
        #print(f"Resp URL:'{response.url}'")
        return response
    def get(self, url, headers=None) -> requests.Response:
        response = requests.get(url, headers=headers)
        return response
    def load_auth_token(self) -> Secret:
        auth_token = Secret(self._settings.auth_token_file)
        return auth_token
    def load_oauth2_secrets(self) -> Mapping[str, Secret]:
        oauth2_id = Secret(self._settings.oauth2_id_file)
        oauth2_secret = Secret(self._settings.oauth2_secret_file)
        return {
            "id": oauth2_id,
            "secret": oauth2_secret
        }
    def load_project_id(self) -> Secret:
        proj_id = Secret(self._settings.project_id_file)
        return proj_id
    def load_refresh_token(self) -> Secret:
        ref_token = Secret(self._settings.refresh_token_file)
        return ref_token
    def refresh_auth_token(self, force=False) -> Secret:
        """Sends a refresh request for the auth token"""
        auth_token = Secret(self._settings.auth_token_file)
        if is_auth_token_valid(auth_token):
            if not force:
                return auth_token
        print("Refreshing auth token",file=sys.stderr)
        oauths = self.load_oauth2_secrets()
        proj_id = self.load_project_id()
        ref_token = self.load_refresh_token()
        oauth2_id = oauths["id"]
        oauth2_secret = oauths["secret"]
        token_params = {
            "client_id": oauth2_id.token,
            "client_secret": oauth2_secret.token,
            "refresh_token": ref_token.token,
            "grant_type": "refresh_token"
        }
        response = self.post(BASE_GOOGLE_AUTH_URL, params=token_params)
        if response.status_code != 200:
            return None
        data = response.json()
        if "access_token" not in data:
            self.error_handler(data)
            return None
        auth_token = Secret(self._settings.auth_token_file)
        auth_token.update_value(data["access_token"], data["expires_in"])
        return auth_token
    def get_devices(self) -> Union[requests.Response, None]:
        proj_id = Secret(self._settings.project_id_file)
        auth_token = self.refresh_auth_token()
        if auth_token is None:
            return None
        # auth_token = Secret(self._settings.auth_token_file)
        # if not is_auth_token_valid(auth_token):
        #     auth_token = self.refresh_auth_token()
        url = f"{BASE_NEST_API_URL}/{proj_id.token}/devices"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {auth_token.token}"
        }
        response = self.get(url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            print(response.json())
        return response
    def get_device_detail(self, device_id: str) -> Union[requests.Response, BaseSensor, Mapping]:
        proj_id = Secret(self._settings.project_id_file)
        auth_token = self.refresh_auth_token()
        if auth_token is None:
            return None
        # auth_token = Secret(self._settings.auth_token_file)
        # if not is_auth_token_valid(auth_token):
        #     auth_token = self.refresh_auth_token()
        url = f"{BASE_NEST_API_URL}/{proj_id.token}/devices/{device_id}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {auth_token.token}"
        }
        response = self.get(url, headers=headers)
        if response.status_code == 200:
            json_resp = response.json()
            if "error" in json_resp:
                self.error_handler(json_resp)
                return response
            cls = CLASS_FOR_SENSOR_TYPE[json_resp["type"]]
            if cls is None:
                return json_resp
            return cls(json_resp)
        return response