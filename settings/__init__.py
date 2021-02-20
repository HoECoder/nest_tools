from typing import Union
import os
import sys
import dotenv

#Root of Secrets
THERMOSTAT_SECRETS_DIR = "THERMOSTAT_SECRETS_DIR"

#OAuth Data
OAUTH2_ID_FILE = "OAUTH2_ID_FILE"
OAUTH2_SECRET_FILE = "OAUTH2_SECRET_FILE"

#Tokens
AUTH_TOKEN_FILE = "AUTH_TOKEN_FILE"
REFRESH_TOKEN_FILE = "REFRESH_TOKEN_FILE"

#Project ID
PROJECT_ID_FILE = "PROJECT_ID_FILE"


class Settings:
    def __init__(self, env_file: Union[str, None]=None):
        self._data = {}
        self._env_file = env_file
        if not self._env_file:
            self._data = dotenv.dotenv_values()
        else:
            self._data = dotenv.dotenv_values(self._env_file)
    @property
    def secrets_dir(self):
        """Directory secrets will be loaded from"""
        return self._data.get(THERMOSTAT_SECRETS_DIR, '')
    @property
    def oauth2_id_file(self):
        return self._data.get(OAUTH2_ID_FILE, '')
    @property
    def oauth2_secret_file(self):
        return self._data.get(OAUTH2_SECRET_FILE, '')
    @property
    def auth_token_file(self):
        return self._data.get(AUTH_TOKEN_FILE, '')
    @property
    def refresh_token_file(self):
        return self._data.get(REFRESH_TOKEN_FILE, '')
    @property
    def project_id_file(self):
        return self._data.get(PROJECT_ID_FILE, '')