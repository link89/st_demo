import streamlit as st

from st_demo import st_extension as st_ext

st.set_page_config(page_title="Streamlit Demo App")

# This should be call at the beginning of the app
web_ctx = st_ext.get_web_context()

# route page by url

st.title("Streamlit Demo App")
st.write("This app is about to show how to work around some streamlit limitations to build a full-fledged web app.")

st.write('## Cookie Based Session')
st.write(f"Session ID: {web_ctx.session_id}, current url is: {web_ctx.url}")
st.write('This session ID will be the same for the same user until the cookies are cleared.')
st.write('You can try to refresh this page or open another tab to see if the session ID remains the same.')

st.write('## Authentication')
st.write('Now that we have session support in streamlit, we can use it to implement authentication.')

st.markdown('''
Here we use GitHub OAuth as an example. The key point is to:
1. Redirect the user to the GitHub OAuth page.
2. After the user logs in, GitHub will redirect the user back to our app with a code.
3. We can use this code to get the user's access token.
4. store the access token and user info in the web session.

Since streamlit does not support redirecting user, so the redirect URL of oauth2 will always be the home page.
''')


