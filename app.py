import streamlit as st

from st_demo import st_extension as st_ext
from st_demo.context import auth_manager

st.set_page_config(page_title="Streamlit Demo App")

# This should be call at the beginning of the app
web_ctx = st_ext.get_web_context()

user = None
logout = st.query_params.get('logout')
code = st.query_params.get('code')
if 'true' == logout:
    auth_manager.logout_user(session_id=web_ctx.session_id)

user = auth_manager.get_or_authenticate_user(session_id=web_ctx.session_id, code=code)


# route page by url
st.title("Streamlit Demo App")

st.markdown(f'''
This app is about to show how to work around some streamlit limitations to build a full-fledged web app.
''')

st.markdown(f'''
## Cookie Based Session
A unique session ID will be generated and set in the cookie when you first visit this page.

Session ID: {web_ctx.session_id}

This session ID will be the same for the same user until the cookies are cleared.
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
    st.write(f'You are not logged in. <a href="{auth_manager.get_oauth2_login_url()}" target="_self">Click to login.</a>', unsafe_allow_html=True)
else:
    st.write(f'You are logged in. Your access token is: {user.access_token}')
    st.write(f'<a href="?logout=true" target="_self">Click to logout</a>.', unsafe_allow_html=True)

st.markdown('''
## Limitations & Known Issues

* Cannot hide auth code in URL after login as there is not way to redirect page. This will cause trouble if the user refresh the page, share the URL or restart streamlit server. Even `st.switch_page` cannot help as it don't clear the query string.
''')