# This file is to initialize components of the app and wire them together.
import streamlit as st

from .auth import AuthManager
from .config import Config

config = Config(st.secrets['config'])
auth_manager = AuthManager(config=config)
