"""
Dynamic Theme System for MIND Dashboard
Provides light/dark mode toggle across all pages
"""

import streamlit as st

# Initialize theme in session state
def init_theme():
    """Initialize theme state if not exists"""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"  # Default to light mode

def get_theme():
    """Get current theme"""
    return st.session_state.get("theme", "light")

def toggle_theme():
    """Toggle between light and dark mode"""
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# Theme CSS configurations
LIGHT_THEME = """
<style>
    /* Main background */
    .stApp {
        background-color: #FFFFFF;
        color: #262730;
    }
    
    /* Content area */
    .block-container {
        background-color: #FFFFFF;
        color: #262730;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F0F2F6;
        color: #262730;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: #262730;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #262730;
    }
    
    [data-testid="stMetricLabel"] {
        color: #595959;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #262730 !important;
    }
    
    /* Text */
    p, span, div {
        color: #262730;
    }
    
    /* Cards/containers */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF;
    }
    
    /* Input fields */
    input, textarea, select {
        background-color: #FFFFFF !important;
        color: #262730 !important;
        border: 1px solid #E0E0E0 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #800020;
        color: #FFFFFF;
        border: none;
    }
    
    .stButton > button:hover {
        background-color: #600018;
    }
    
    /* Dataframes */
    .dataframe {
        background-color: #FFFFFF !important;
        color: #262730 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #F0F2F6;
        color: #262730;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F0F2F6;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #262730;
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess, .stInfo, .stWarning, .stError {
        background-color: #F0F2F6;
        color: #262730;
    }
</style>
"""

DARK_THEME = """
<style>
    /* Main background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Content area */
    .block-container {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #262730;
        color: #FAFAFA;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: #FAFAFA;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #FAFAFA;
    }
    
    [data-testid="stMetricLabel"] {
        color: #BDBDBD;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FAFAFA !important;
    }
    
    /* Text */
    p, span, div {
        color: #FAFAFA;
    }
    
    /* Cards/containers */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #1E1E1E;
    }
    
    /* Input fields */
    input, textarea, select {
        background-color: #262730 !important;
        color: #FAFAFA !important;
        border: 1px solid #4A4A4A !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #800020;
        color: #FFFFFF;
        border: none;
    }
    
    .stButton > button:hover {
        background-color: #A00028;
    }
    
    /* Dataframes */
    .dataframe {
        background-color: #1E1E1E !important;
        color: #FAFAFA !important;
    }
    
    .dataframe thead th {
        background-color: #262730 !important;
        color: #FAFAFA !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #262730;
        color: #FAFAFA;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #262730;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #FAFAFA;
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess {
        background-color: #1B4332;
        color: #FAFAFA;
    }
    
    .stInfo {
        background-color: #1E3A5F;
        color: #FAFAFA;
    }
    
    .stWarning {
        background-color: #5F3A1E;
        color: #FAFAFA;
    }
    
    .stError {
        background-color: #5F1E1E;
        color: #FAFAFA;
    }
    
    /* Plotly charts background */
    .js-plotly-plot .plotly {
        background-color: transparent !important;
    }
</style>
"""

def apply_theme():
    """Apply current theme CSS"""
    init_theme()
    theme = get_theme()
    
    if theme == "dark":
        st.markdown(DARK_THEME, unsafe_allow_html=True)
    else:
        st.markdown(LIGHT_THEME, unsafe_allow_html=True)

def create_theme_toggle():
    """Create theme toggle widget"""
    init_theme()
    
    # Create toggle in sidebar
    current_theme = get_theme()
    
    col1, col2 = st.sidebar.columns([3, 1])
    
    with col1:
        st.sidebar.markdown("### 🎨 Theme")
    
    with col2:
        # Toggle button
        is_dark = st.sidebar.toggle(
            "Dark",
            value=(current_theme == "dark"),
            key="theme_toggle",
            help="Toggle between light and dark mode"
        )
        
        # Update theme based on toggle
        new_theme = "dark" if is_dark else "light"
        
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            st.rerun()

def get_plotly_theme():
    """Get Plotly theme configuration based on current theme"""
    theme = get_theme()
    
    if theme == "dark":
        return {
            'layout': {
                'paper_bgcolor': '#0E1117',
                'plot_bgcolor': '#0E1117',
                'font': {'color': '#FAFAFA'},
                'xaxis': {
                    'gridcolor': '#262730',
                    'zerolinecolor': '#262730'
                },
                'yaxis': {
                    'gridcolor': '#262730',
                    'zerolinecolor': '#262730'
                }
            }
        }
    else:
        return {
            'layout': {
                'paper_bgcolor': '#FFFFFF',
                'plot_bgcolor': '#FFFFFF',
                'font': {'color': '#262730'},
                'xaxis': {
                    'gridcolor': '#E0E0E0',
                    'zerolinecolor': '#E0E0E0'
                },
                'yaxis': {
                    'gridcolor': '#E0E0E0',
                    'zerolinecolor': '#E0E0E0'
                }
            }
        }

def get_chart_colors():
    """Get chart colors based on current theme"""
    theme = get_theme()
    
    if theme == "dark":
        return {
            'primary': '#800020',
            'secondary': '#FFD700',
            'accent': '#4169E1',
            'success': '#28A745',
            'warning': '#FFC107',
            'danger': '#DC3545',
            'text': '#FAFAFA',
            'background': '#0E1117'
        }
    else:
        return {
            'primary': '#800020',
            'secondary': '#FFD700',
            'accent': '#4169E1',
            'success': '#28A745',
            'warning': '#FFC107',
            'danger': '#DC3545',
            'text': '#262730',
            'background': '#FFFFFF'
        }
