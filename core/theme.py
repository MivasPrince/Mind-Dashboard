"""
Theme management for MIND Dashboard
Handles dark mode toggle and theme-aware styling
"""

import streamlit as st

def initialize_theme():
    """Initialize theme in session state"""
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False

def toggle_theme():
    """Toggle between light and dark mode"""
    st.session_state.dark_mode = not st.session_state.dark_mode

def get_current_theme():
    """Get current theme name"""
    return 'dark' if st.session_state.get('dark_mode', False) else 'light'

def get_logo_path():
    """Get appropriate logo path based on current theme"""
    from pathlib import Path
    theme = get_current_theme()
    
    if theme == 'dark':
        logo_path = Path(__file__).parent.parent / "assets" / "miva_logo_dark.png"
    else:
        logo_path = Path(__file__).parent.parent / "assets" / "miva_logo_light.png"
    
    # Fallback to generic logo if theme-specific doesn't exist
    if not logo_path.exists():
        logo_path = Path(__file__).parent.parent / "assets" / "miva_logo.png"
    
    return logo_path if logo_path.exists() else None

def apply_theme_css():
    """Apply theme-specific CSS styling"""
    theme = get_current_theme()
    
    if theme == 'dark':
        css = """
        <style>
        /* Dark Mode Styles */
        .main {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #E31837;
            margin-bottom: 1rem;
        }
        .metric-card {
            background-color: #262730;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #E31837;
            color: #FAFAFA;
        }
        .stButton>button {
            width: 100%;
            background-color: #262730;
            color: #FAFAFA;
            border: 1px solid #444;
        }
        .stButton>button:hover {
            background-color: #E31837;
            color: #FFFFFF;
            border: 1px solid #E31837;
        }
        div[data-testid="stMetricValue"] {
            color: #FAFAFA;
        }
        div[data-testid="stMetricLabel"] {
            color: #CCCCCC;
        }
        .stDataFrame {
            background-color: #262730;
        }
        .stMarkdown {
            color: #FAFAFA;
        }
        /* Sidebar dark mode */
        section[data-testid="stSidebar"] {
            background-color: #1a1a1a;
        }
        section[data-testid="stSidebar"] .stMarkdown {
            color: #FAFAFA;
        }
        /* Input fields */
        .stTextInput>div>div>input {
            background-color: #262730;
            color: #FAFAFA;
            border: 1px solid #444;
        }
        .stSelectbox>div>div>div {
            background-color: #262730;
            color: #FAFAFA;
        }
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #262730;
            color: #FAFAFA;
        }
        /* Tables */
        .dataframe {
            color: #FAFAFA !important;
        }
        .dataframe th {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        .dataframe td {
            background-color: #1a1a1a !important;
            color: #FAFAFA !important;
        }
        </style>
        """
    else:
        css = """
        <style>
        /* Light Mode Styles */
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #E31837;
            margin-bottom: 1rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #E31837;
        }
        .stButton>button {
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #E31837;
            color: #FFFFFF;
        }
        </style>
        """
    
    st.markdown(css, unsafe_allow_html=True)

def render_theme_toggle():
    """Render theme toggle button in sidebar"""
    theme = get_current_theme()
    icon = "🌙" if theme == 'light' else "☀️"
    label = "Dark Mode" if theme == 'light' else "Light Mode"
    
    if st.button(f"{icon} {label}", key="theme_toggle", use_container_width=True):
        toggle_theme()
        st.rerun()

def get_theme_colors():
    """Get color scheme based on current theme"""
    theme = get_current_theme()
    
    if theme == 'dark':
        return {
            'background': '#0E1117',
            'secondary_bg': '#262730',
            'text': '#FAFAFA',
            'text_secondary': '#CCCCCC',
            'primary': '#E31837',
            'border': '#444444'
        }
    else:
        return {
            'background': '#FFFFFF',
            'secondary_bg': '#F0F2F6',
            'text': '#262730',
            'text_secondary': '#666666',
            'primary': '#E31837',
            'border': '#DDDDDD'
        }
