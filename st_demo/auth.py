from .config import Config


class AuthManager:
    def __init__(self, config: Config):
        self.config = config
        self.users = {}
        self.sessions = {}

    def get_user(self, session_id):
        return self.users.get(session_id, None)

    def oauth2_login(self, session_id: str, code: str):
        oauth2_provider: dict = self.config.data.get('oauth2_provider')
        if oauth2_provider is None:
            raise ValueError('oauth2_provider is not configured')
