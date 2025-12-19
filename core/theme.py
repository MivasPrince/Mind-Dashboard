import streamlit as st


def apply_theme():
    """
    Injects global CSS and ensures brand consistency.
    Called at the top of every page (already done in Home.py).
    """

    primary = "#ecf1f3"
    secondary = "#203891"
    accent = "#bd300e"
    text_color = "#232020"
    background = "#ffffff"

    css = f"""
        <style>

        /* Global background */
        .stApp {{
            background-color: {background} !important;
        }}

        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: {primary} !important;
        }}

        /* Headers */
        h1, h2, h3, h4 {{
            color: {secondary} !important;
        }}

        /* Body text */
        p, span, div {{
            color: {text_color} !important;
        }}

        /* Buttons */
        .stButton>button {{
            background-color: {secondary} !important;
            color: white !important;
            border-radius: 6px !important;
            border: none !important;
        }}

        .stButton>button:hover {{
            background-color: {accent} !important;
            color: white !important;
        }}

        /* Tables */
        table {{
            color: {text_color} !important;
        }}

        </style>
    """

    st.markdown(css, unsafe_allow_html=True)

