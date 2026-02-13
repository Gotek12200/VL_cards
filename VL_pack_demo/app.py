import streamlit as st

from views.pack_demo_tab import render as render_pack_demo
from views.future_tab import render as render_future

st.set_page_config(page_title="VL Pack Opening Demo", layout="centered")

st.title("VL Cards Pack Opening Demo")

tab1, tab2 = st.tabs(["Pack Opening", "Future Stuff"])

with tab1:
    render_pack_demo()

with tab2:
    render_future()
