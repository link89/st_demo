from typing import Optional, Mapping
from pydantic import BaseModel

import requests

from .config import Config


class OAuth2Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int = 0


class AuthManager:
    def __init__(self, config: Config):
        self.oauth2_provider = config.data.oauth2_provider
        self.users = {}
        self.sessions: Mapping[str, OAuth2Token] = {}

    def get_oauth2_login_url(self):
        return f'{self.oauth2_provider.login_url}?client_id={self.oauth2_provider.client_id}'

    def get_oauth2_token(self, code):
        res = requests.post(self.oauth2_provider.access_token_url, params={
            'client_id': self.oauth2_provider.client_id,
            'client_secret': self.oauth2_provider.client_secret,
            'code': code,
            'redirect_uri': self.oauth2_provider.redirect_uri,
        })
        return OAuth2Token(**res.json())

    def get_or_authenticate_user(self, session_id, code = None) -> Optional[OAuth2Token]:
        if session_id in self.sessions:
            return self.sessions[session_id]
        if code is None:
            return None
        token = self.get_oauth2_token(code)
        self.sessions[session_id] = token
        return token
