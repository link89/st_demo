from typing import Optional, Mapping
from pydantic import BaseModel
from urllib.parse import parse_qsl

import requests

from .config import Config


class OAuth2Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int = 0


class User:
    def get_profile(self):
        raise NotImplementedError


class OAuth2User(User):
    def __init__(self, token: OAuth2Token):
        self.token = token


class AuthManager:
    def __init__(self, config: Config):
        self.oauth2_provider = config.data.oauth2_provider
        self.users = {}
        self.sessions: Mapping[str, OAuth2Token] = {}
        self.used_code = set()

    def get_oauth2_login_url(self):
        return f'{self.oauth2_provider.login_url}?client_id={self.oauth2_provider.client_id}'

    def get_oauth2_token(self, code):
        res = requests.post(self.oauth2_provider.access_token_url, params={
            'code': code,
            'client_id': self.oauth2_provider.client_id,
            'client_secret': self.oauth2_provider.client_secret,
            'redirect_uri': self.oauth2_provider.redirect_uri,
        })
        if 'application/json' in res.headers['Content-Type']:
            data = res.json()
        elif 'application/x-www-form-urlencoded' in res.headers['Content-Type']:
            data = dict(parse_qsl(res.text))
        else:
            raise ValueError(f'Unsupported content type: {res.headers["Content-Type"]}')
        return OAuth2Token(**data)

    def get_or_authenticate_user(self, session_id, code = None) -> Optional[OAuth2Token]:
        if session_id in self.sessions:
            return self.sessions[session_id]
        if code is None or code in self.used_code:
            return None
        # FIXME: this will cause memory leak
        self.used_code.add(code)
        token = self.get_oauth2_token(code)
        self.sessions[session_id] = token
        return token

    def logout_user(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
