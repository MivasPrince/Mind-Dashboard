"""
Theme configuration for MIND Unified Dashboard
Dynamic Light/Dark Mode Support with Miva Branding
"""

import streamlit as st

# Import theme toggle system
try:
    from theme_toggle import get_theme, get_chart_colors as get_dynamic_colors
    DYNAMIC_THEME = True
except ImportError:
    DYNAMIC_THEME = False

# Miva University Brand Colors (used in both themes)
BRAND_COLORS = {
    'primary': '#800020',      # Miva Burgundy
    'secondary': '#FFD700',    # Miva Gold
    'accent': '#4169E1',       # Royal Blue
    'success': '#28A745',      # Green
    'warning': '#FFC107',      # Amber
    'danger': '#DC3545',       # Red
}

# Light Theme Colors
LIGHT_COLORS = {
    **BRAND_COLORS,
    'background': '#FFFFFF',
    'secondary_bg': '#F5F5F5',
    'text': '#2C3E50',
    'text_light': '#6C757D',
    'border': '#DEE2E6',
    'white': '#FFFFFF',
}

# Dark Theme Colors
DARK_COLORS = {
    **BRAND_COLORS,
    'background': '#0E1117',
    'secondary_bg': '#262730',
    'text': '#FAFAFA',
    'text_light': '#BDBDBD',
    'border': '#4A4A4A',
    'white': '#1E1E1E',
}

# Get current theme colors
def get_colors():
    """Get color scheme based on current theme"""
    if DYNAMIC_THEME:
        theme = get_theme()
        return DARK_COLORS if theme == "dark" else LIGHT_COLORS
    return LIGHT_COLORS

# Export COLORS for backward compatibility
COLORS = get_colors()

# Chart color schemes
CHART_COLORS = {
    'primary_gradient': ['#800020', '#A00028', '#C00030', '#E00038'],
    'secondary_gradient': ['#FFD700', '#FFE44D', '#FFF199', '#FFFFE6'],
    'mixed': ['#800020', '#4169E1', '#28A745', '#FFC107', '#DC3545'],
    'performance': ['#DC3545', '#FFC107', '#28A745'],  # Red -> Yellow -> Green
}

def get_plotly_theme():
    """Returns Plotly theme configuration based on current mode"""
    colors = get_colors()
    
    return {
        'layout': {
            'paper_bgcolor': colors['background'],
            'plot_bgcolor': colors['background'],
            'font': {
                'family': 'Inter, sans-serif',
                'color': colors['text']
            },
            'title': {
                'font': {
                    'size': 18,
                    'color': colors['primary'],
                    'family': 'Inter, sans-serif'
                }
            },
            'xaxis': {
                'gridcolor': colors['border'],
                'linecolor': colors['border'],
                'tickfont': {'color': colors['text']}
            },
            'yaxis': {
                'gridcolor': colors['border'],
                'linecolor': colors['border'],
                'tickfont': {'color': colors['text']}
            },
            'colorway': CHART_COLORS['primary_gradient'],
            'hovermode': 'closest',
            'hoverlabel': {
                'bgcolor': colors['background'],
                'font': {'color': colors['text']}
            },
            'legend': {
                'font': {'color': colors['text']}
            }
        }
    }

def apply_streamlit_theme():
    """Returns CSS for Streamlit custom theming - static styles only"""
    colors = get_colors()
    
    return f"""
    <style>
        /* KPI cards */
        .kpi-card {{
            background-color: {colors['white']};
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid {colors['primary']};
        }}
        
        /* Accent elements */
        .accent-border {{
            border-left: 4px solid {colors['accent']};
        }}
        
        /* Metric containers */
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            font-weight: 600;
        }}
        
        /* Data tables */
        .dataframe {{
            border: 1px solid {colors['border']};
            border-radius: 5px;
        }}
        
        /* Remove Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {colors['secondary_bg']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {colors['primary']};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: #600018;
        }}
    </style>
    """
