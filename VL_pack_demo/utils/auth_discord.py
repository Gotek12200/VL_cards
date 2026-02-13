import secrets
import time
import requests
import streamlit as st
from urllib.parse import urlencode

DISCORD_AUTH_URL = "https://discord.com/api/oauth2/authorize"
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_API_ME = "https://discord.com/api/users/@me"

def _get_conf():
    return {
        "client_id": st.secrets["DISCORD_CLIENT_ID"],
        "client_secret": st.secrets["DISCORD_CLIENT_SECRET"],
        "redirect_uri": st.secrets["DISCORD_REDIRECT_URI"],
        "state_secret": st.secrets["DISCORD_STATE_SECRET"],
    }

def build_login_url() -> str:
    conf = _get_conf()

    # CSRF protection: store a random state in session
    state = secrets.token_urlsafe(24)
    st.session_state["oauth_state"] = state
    st.session_state["oauth_state_time"] = int(time.time())

    params = {
        "client_id": conf["client_id"],
        "redirect_uri": conf["redirect_uri"],
        "response_type": "code",
        "scope": "identify",
        "state": state,
        # optional: "prompt": "consent"
    }
    return f"{DISCORD_AUTH_URL}?{urlencode(params)}"

def handle_discord_callback():
    """
    If Discord redirected back with ?code=...&state=..., exchange for token and fetch user.
    On success sets st.session_state["user"].
    """
    qp = st.query_params  # Streamlit query params (new API)
    code = qp.get("code")
    state = qp.get("state")

    if not code:
        return  # nothing to do

    expected_state = st.session_state.get("oauth_state")
    if not expected_state or state != expected_state:
        st.error("Invalid login state. Please try logging in again.")
        clear_oauth_query_params()
        return

    conf = _get_conf()

    data = {
        "client_id": conf["client_id"],
        "client_secret": conf["client_secret"],
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": conf["redirect_uri"],
        "scope": "identify",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_res = requests.post(DISCORD_TOKEN_URL, data=data, headers=headers, timeout=15)

    if token_res.status_code != 200:
        st.error(f"Token exchange failed: {token_res.status_code}")
        clear_oauth_query_params()
        return

    token_json = token_res.json()
    access_token = token_json.get("access_token")
    if not access_token:
        st.error("No access token returned.")
        clear_oauth_query_params()
        return

    me_res = requests.get(
        DISCORD_API_ME,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )

    if me_res.status_code != 200:
        st.error(f"Failed to fetch user: {me_res.status_code}")
        clear_oauth_query_params()
        return

    user = me_res.json()
    # user has: id, username, global_name (optional), avatar, etc.

    st.session_state["user"] = {
        "id": user.get("id"),
        "username": user.get("username"),
        "global_name": user.get("global_name"),
        "avatar": user.get("avatar"),
    }

    # cleanup
    clear_oauth_query_params()
    st.rerun()

def clear_oauth_query_params():
    # remove ?code=&state= from URL after login
    st.query_params.clear()

def logout():
    st.session_state.pop("user", None)
    st.session_state.pop("oauth_state", None)
    st.session_state.pop("oauth_state_time", None)
    st.rerun()

def avatar_url(user_id: str, avatar_hash: str | None) -> str | None:
    if not user_id or not avatar_hash:
        return None
    return f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png"
