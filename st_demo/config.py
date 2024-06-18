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
    def __init__(self, config_file):
        self.config_file = config_file
        with open(self.config_file, 'r') as f:
            data = yaml.safe_load(f)
        self.data = ConfigModel(**data)
