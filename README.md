# Streamlit Demo

## Description
This is a demo project to show how to use Streamlit to build a web app with session and authentication support.

## Getting Started

Setup a virtual environment using poetry:

```bash
poetry install
```

This app use GitHub App as OAuth2 provider. 
To run the app, you need to create a GitHub App first.

And then create a `config.yml` file in the project root with the following content:
```yaml
oauth2_provider:
  client_id: <your_client_id>
  client_secret: <your_client_secret>
  login_url: https://github.com/login/oauth/authorize
  access_token_url: https://github.com/login/oauth/access_token
  redirect_uri: http://localhost:8051/  # change this to your actual redirect uri
```
