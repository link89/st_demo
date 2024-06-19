import streamlit as st
from pydantic import BaseModel
import yaml


class OAuth2Provider(BaseModel):
    client_id: str
    client_secret: str
    login_url: str
    access_token_url: str
    redirect_uri: str


class ConfigModel(BaseModel):
    oauth2_provider: OAuth2Provider


class Config:
    def __init__(self, config_str: str):
        data = yaml.safe_load(config_str)
        self.data = ConfigModel(**data)
