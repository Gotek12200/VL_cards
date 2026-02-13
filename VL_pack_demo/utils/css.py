import streamlit as st

def inject_global_css():
    st.markdown(
        """
        <style>
        @keyframes pop {
            0% { transform: scale(0.5); opacity:0; }
            100% { transform: scale(1); opacity:1; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
