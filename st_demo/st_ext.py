import streamlit as st

from http.cookies import SimpleCookie
from streamlit.web.server.websocket_headers import _get_websocket_headers


def get_cookie():
    headers = _get_websocket_headers()
    cookie_str = headers.get("Cookie")
    if cookie_str:
        return SimpleCookie(cookie_str)

    
