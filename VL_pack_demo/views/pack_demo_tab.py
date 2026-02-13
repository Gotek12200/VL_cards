import streamlit as st
from utils.css import inject_global_css
from components.pack_opening import run_pack_open_sequence

def render():
    inject_global_css()

    st.write("Press OPEN PACK to open a pack")

    if st.button("OPEN PACK"):
        run_pack_open_sequence()
