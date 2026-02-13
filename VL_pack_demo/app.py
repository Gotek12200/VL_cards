import streamlit as st

from utils.auth_discord import handle_discord_callback, logout, avatar_url
from views.login_view import render as render_login
from views.pack_demo_tab import render as render_pack_demo
from views.future_tab import render as render_future

st.set_page_config(page_title="VL Pack Opening Demo", layout="centered")

# If Discord redirected back, this will capture code/state and log user in
handle_discord_callback()

user = st.session_state.get("user")

if not user:
    render_login()
    st.stop()

# Logged in UI header
name = user.get("global_name") or user.get("username")
st.title(f"VL Cards — Welcome, {name}!")

av = avatar_url(user.get("id"), user.get("avatar"))
if av:
    st.image(av, width=72)

if st.button("Logout"):
    logout()

tab1, tab2 = st.tabs(["Pack Opening", "Future Stuff"])
with tab1:
    render_pack_demo()
with tab2:
    render_future()
