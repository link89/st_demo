import streamlit as st

from st_demo import st_extension as st_ext
from st_demo.context import auth_manager

st.set_page_config(page_title="Streamlit Demo App")

# This must be call at the beginning of the page
session_id = st_ext.get_web_session()

# TODO: move the logout logic to a dedicated page
logout = st.query_params.pop('logout', None)
if 'true' == logout:
    auth_manager.logout_user(session_id=session_id)

# TODO: move the login logic to a dedicated page
user = None
code = st.query_params.pop('code', None)
user = auth_manager.get_or_authenticate_user(session_id=session_id, code=code)

# Start to build page
st.title("Streamlit Demo App")

st.markdown(f'''
This app is about to show how to work around some streamlit limitations to build a full-fledged web app.
''')

st.markdown(f'''
## Cookie Based Session
A unique session ID will be generated and set in the cookie when you first visit this page.

Session ID: {session_id}

This session ID will be the same for the same user until the cookie is cleared or expired.
You can try to refresh this page or open another tab to see if the session ID remains the same.
''')

st.write('## Session Based Authentication')
st.markdown('''
Now that we have session support in streamlit, we can use it to implement authentication.

Note that this is **NOT** token based authentication,
the access token won't be stored in the client.
Don't do things like setting the access token in cookie or localstorage.

The access token should be stored in the server side.
And then client use session ID to access the server side data.

Here we use GitHub App as an example. The key point is to:
1. Click login to access GitHub OAuth2 login page.
2. After the user logs in, GitHub will redirect the user back to our app with a code.
3. We can use this code to get the user's access token.
4. Store the access token and user info in the server.

''')

if user is None:
    st.write(f'You are not logged in.')
    st.write(f'<a href="{auth_manager.get_oauth2_login_url()}" target="_self">Click to login.</a>', unsafe_allow_html=True)
else:
    st.write(f'You are logged in. Your access token is: {user.access_token}')
    st.write(f'<a href="?logout=true" target="_self">Click to logout</a>.', unsafe_allow_html=True)