from pathlib import Path

import streamlit as st


def load_css(css_path: str = "assets/styles.css"):
    """
    Load custom CSS into Streamlit.
    """

    path = Path(css_path)

    if path.exists():
        css = path.read_text(encoding="utf-8")

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True,
        )