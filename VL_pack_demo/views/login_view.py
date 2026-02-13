import streamlit as st
from utils.auth_discord import build_login_url

def render():
    st.header("Login required")
    st.write("To continue, please sign in with Discord.")

    login_url = build_login_url()

    # Streamlit button that links out
    st.link_button("Login with Discord", login_url, use_container_width=True)

    st.caption("You’ll be redirected back here after approving access.")
