from streamlit.web.server.websocket_headers import _get_websocket_headers
from streamlit.components.v1 import html
import streamlit as st

from collections import namedtuple
from http.cookies import SimpleCookie
from uuid import uuid4
from time import sleep
import urllib.parse


def get_cookie():
    headers = _get_websocket_headers()  # this will be None for streamlit cloud
    if headers is not None:
        cookie_str = headers.get("Cookie")
        if cookie_str:
            return SimpleCookie(cookie_str)


def get_cookie_value(key):
    cookie = get_cookie()
    if cookie is not None:
        cookie_value = cookie.get(key)
        if cookie_value is not None:
            return cookie_value.value
    return None


def get_web_session():
    if 'st_session_id' not in st.session_state:
        session_id = get_cookie_value('ST_SESSION_ID')

        if session_id is None:
            # fallback to streamlit_session for streamlit cloud
            session_id = get_cookie_value('streamlit_session')

        if session_id is None:
            session_id = uuid4().hex
            st.session_state['st_session_id'] = session_id
            html(f'<script>document.cookie = "ST_SESSION_ID={session_id}";</script>')
            sleep(0.1)  # FIXME: workaround around bug: Tried to use SessionInfo before it was initialized
            st.rerun()  # FIXME: rerun immediately so that html won't be shown in the final page
        st.session_state['st_session_id'] = session_id
    return st.session_state['st_session_id']


def get_current_url():
    session = st.runtime.get_instance()._session_mgr.list_active_sessions()[0]
    return urllib.parse.urlunparse([session.client.request.protocol, session.client.request.host, "", "", "", ""])


WebContext = namedtuple('WebContext', ['session_id', 'url'])

def get_web_context():
    return WebContext(session_id=get_web_session(), url=get_current_url())
