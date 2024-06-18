# This file is to initialize components of the app and wire them together.

from .auth import AuthManager
from .config import Config

config = Config('config.yml')

auth_manager = AuthManager()

