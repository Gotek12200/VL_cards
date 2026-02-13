import base64
import streamlit as st
from utils.paths import ROOT

def img_data_uri(rel_path: str) -> str:
    p = ROOT / rel_path
    data = p.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:image/png;base64,{b64}"

def play_sound(rel_path: str):
    audio_bytes = (ROOT / rel_path).read_bytes()
    b64 = base64.b64encode(audio_bytes).decode("utf-8")
    st.markdown(
        f"""
        <audio autoplay>
          <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True
    )
