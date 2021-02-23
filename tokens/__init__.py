"""Lib for token management"""

from enum import Enum
from types import SimpleNamespace
import time
import toml

class SecretTypes(Enum):
    Auth_Token = "Auth"
    Refresh_Token = "Refresh"
    Project_ID = "Project ID"
    OAuth2_ID = "OAuth2 ID"
    OAuth2_Secret = "OAuth2 Secret"

TOKENS_WITH_TTL = [
    SecretTypes.Auth_Token.value
]

class Secret:
    def __init__(self, filename):
        self._filename = filename
        self._dat = None
        self.load_from_file()
    def file_not_found_callback(self):
        pass
    def load_from_file(self):
        try:
            data = toml.load(self._filename)
            token = data.get("Secret")
            token_type = data.get("Type")
            token_life = data.get("Lifetime")
            token_created = data.get("Created")
            self._dat = SimpleNamespace(token=token,
                                        token_type=token_type,
                                        token_life=token_life,
                                        token_created=token_created)
        except FileNotFoundError:
            self.file_not_found_callback()
    @property
    def token(self):
        return self._dat.token
    @property
    def token_type(self):
        return self._dat.token_type
    @property
    def token_life(self):
        return self._dat.token_life
    @property
    def token_created(self):
        return self._dat.token_created
    def update_value(self, value, ttl):
        now = int(time.time())
        self._dat.token = value
        self._dat.token_life = ttl
        self._dat.token_created = now
        token_dat = {
            "Secret": self.token,
            "Type": self.token_type,
            "Lifetime": self.token_life,
            "Created": self.token_created
        }
        with open(self._filename, "w") as _token_file:
            toml.dump(token_dat, _token_file)
    
    