from pydantic import BaseModel
import yaml


class GithubAppAuth(BaseModel):
    app_id: int
    app_private_key: str
    app_installation_id: int
    app_installation_token: str


class ConfigModel(BaseModel):
    github_app_auth: GithubAppAuth


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        with open(self.config_file, 'r') as f:
            data = yaml.safe_load(f)
        self.data = ConfigModel(**data)
