"""
Enhanced UI Components for MIND Analytics Dashboard
Comprehensive visualization library with export, interactivity, and advanced charts
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import io
from core.settings import COLORS
from core.theme import get_current_theme, get_theme_colors

# ============================================================================
# KPI CARDS & METRICS
# ============================================================================

def render_kpi_card(title: str, value: any, delta: Optional[str] = None, 
                   help_text: Optional[str] = None, icon: str = "📊"):
    """Render a single KPI metric card"""
    with st.container():
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown(f"<h1>{icon}</h1>", unsafe_allow_html=True)
        with col2:
            if delta:
                st.metric(label=title, value=value, delta=delta, help=help_text)
            else:
                st.metric(label=title, value=value, help=help_text)

def render_kpi_row(kpis: list):
    """Render a row of KPI cards"""
    cols = st.columns(len(kpis))
    for i, kpi in enumerate(kpis):
        with cols[i]:
            render_kpi_card(
                title=kpi.get('title', ''),
                value=kpi.get('value', 0),
                delta=kpi.get('delta'),
                help_text=kpi.get('help_text'),
                icon=kpi.get('icon', '📊')
            )

def render_gauge_chart(title: str, value: float, max_value: float = 100, 
                       threshold_colors: Optional[Dict] = None):
    """Render a gauge/indicator chart"""
    if threshold_colors is None:
        threshold_colors = {'low': 'red', 'medium': 'yellow', 'high': 'green'}
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        gauge = {
            'axis': {'range': [None, max_value]},
            'bar': {'color': COLORS['primary']},
            'steps': [
                {'range': [0, max_value * 0.33], 'color': "lightgray"},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# GLOBAL FILTERS
# ============================================================================

def render_global_filters(show_date: bool = True, show_case_study: bool = True,
                         show_cohort: bool = True, show_role: bool = True,
                         show_session_type: bool = False):
    """Render global filter panel"""
    st.markdown("### 🔍 Filters")
    
    filters = {}
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if show_date:
            date_range = st.selectbox(
                "Date Range",
                ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time", "Custom"],
                key="global_date_filter"
            )
            filters['date_range'] = date_range
            
            if date_range == "Custom":
                start_date = st.date_input("Start Date", key="filter_start_date")
                end_date = st.date_input("End Date", key="filter_end_date")
                filters['start_date'] = start_date
                filters['end_date'] = end_date
    
    with col2:
        if show_case_study:
            case_study = st.selectbox(
                "Case Study",
                ["All Case Studies", "Case Study 1", "Case Study 2"],  # Will be populated from data
                key="global_case_filter"
            )
            filters['case_study'] = case_study
        
        if show_cohort:
            cohort = st.selectbox(
                "Cohort",
                ["All Cohorts", "2024-A", "2024-B", "2025-A"],  # Will be populated from data
                key="global_cohort_filter"
            )
            filters['cohort'] = cohort
    
    with col3:
        if show_role:
            role = st.selectbox(
                "User Role",
                ["All Roles", "Student", "Faculty", "Admin"],
                key="global_role_filter"
            )
            filters['role'] = role
        
        if show_session_type:
            session_type = st.selectbox(
                "Session Type",
                ["All Types", "Learning", "Exploratory", "Navigation Only"],
                key="global_session_type_filter"
            )
            filters['session_type'] = session_type
    
    return filters

# ============================================================================
# CHART RENDERERS
# ============================================================================

def render_line_chart(data: pd.DataFrame, x: str, y: str, title: str,
                     color: Optional[str] = None, height: int = 400):
    """Render interactive line chart"""
    theme_colors = get_theme_colors()
    
    if color:
        fig = px.line(data, x=x, y=y, color=color, title=title)
    else:
        fig = px.line(data, x=x, y=y, title=title)
    
    fig.update_traces(line_color=COLORS['primary'])
    fig.update_layout(
        height=height,
        hovermode='x unified',
        plot_bgcolor=theme_colors['bg'],
        paper_bgcolor=theme_colors['bg']
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_bar_chart(data: pd.DataFrame, x: str, y: str, title: str,
                    color: Optional[str] = None, orientation: str = 'v', height: int = 400):
    """Render interactive bar chart"""
    theme_colors = get_theme_colors()
    
    fig = px.bar(data, x=x, y=y, color=color, title=title, orientation=orientation)
    fig.update_traces(marker_color=COLORS['primary'])
    fig.update_layout(
        height=height,
        plot_bgcolor=theme_colors['bg'],
        paper_bgcolor=theme_colors['bg']
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_scatter_plot(data: pd.DataFrame, x: str, y: str, title: str,
                       color: Optional[str] = None, size: Optional[str] = None,
                       height: int = 400):
    """Render scatter plot"""
    theme_colors = get_theme_colors()
    
    fig = px.scatter(data, x=x, y=y, color=color, size=size, title=title)
    fig.update_layout(
        height=height,
        plot_bgcolor=theme_colors['bg'],
        paper_bgcolor=theme_colors['bg']
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_box_plot(data: pd.DataFrame, x: str, y: str, title: str,
                   color: Optional[str] = None, height: int = 400):
    """Render box plot for distribution analysis"""
    theme_colors = get_theme_colors()
    
    fig = px.box(data, x=x, y=y, color=color, title=title)
    fig.update_layout(
        height=height,
        plot_bgcolor=theme_colors['bg'],
        paper_bgcolor=theme_colors['bg']
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_histogram(data: pd.DataFrame, x: str, title: str,
                    nbins: int = 30, height: int = 400):
    """Render histogram for distribution"""
    theme_colors = get_theme_colors()
    
    fig = px.histogram(data, x=x, title=title, nbins=nbins)
    fig.update_traces(marker_color=COLORS['primary'])
    fig.update_layout(
        height=height,
        plot_bgcolor=theme_colors['bg'],
        paper_bgcolor=theme_colors['bg']
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_area_chart(data: pd.DataFrame, x: str, y: str, title: str,
                     color: Optional[str] = None, height: int = 400):
    """Render stacked area chart"""
    theme_colors = get_theme_colors()
    
    fig = px.area(data, x=x, y=y, color=color, title=title)
    fig.update_layout(
        height=height,
        plot_bgcolor=theme_colors['bg'],
        paper_bgcolor=theme_colors['bg']
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_pie_chart(data: pd.DataFrame, values: str, names: str, title: str,
                    height: int = 400):
    """Render pie chart"""
    theme_colors = get_theme_colors()
    
    fig = px.pie(data, values=values, names=names, title=title)
    fig.update_layout(
        height=height,
        plot_bgcolor=theme_colors['bg'],
        paper_bgcolor=theme_colors['bg']
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_heatmap(data: pd.DataFrame, x: str, y: str, z: str, title: str,
                  height: int = 500):
    """Render heatmap"""
    theme_colors = get_theme_colors()
    
    # Pivot data for heatmap
    pivot_data = data.pivot(index=y, columns=x, values=z)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='Reds'
    ))
    
    fig.update_layout(
        title=title,
        height=height,
        plot_bgcolor=theme_colors['bg'],
        paper_bgcolor=theme_colors['bg']
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_radar_chart(categories: List[str], values: List[float], title: str,
                      height: int = 400):
    """Render radar chart for multi-dimensional comparison"""
    theme_colors = get_theme_colors()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line_color=COLORS['primary']
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=False,
        title=title,
        height=height
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_funnel_chart(stages: List[str], values: List[int], title: str,
                       height: int = 400):
    """Render funnel chart for conversion analysis"""
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial"
    ))
    
    fig.update_layout(
        title=title,
        height=height
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# DATA TABLES WITH EXPORT
# ============================================================================

def render_data_table(data: pd.DataFrame, title: str = "Data Table",
                     max_rows: int = 100, enable_download: bool = True,
                     key_suffix: str = ""):
    """Render interactive data table with export functionality"""
    
    st.markdown(f"#### {title}")
    
    if data is None or data.empty:
        st.info("No data available")
        return
    
    # Display controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.dataframe(data.head(max_rows), use_container_width=True, hide_index=True)
        
        if len(data) > max_rows:
            st.caption(f"Showing {max_rows} of {len(data)} rows")
    
    with col2:
        if enable_download:
            # CSV Download
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key=f"csv_download_{key_suffix}"
            )
            
            # Excel Download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, index=False, sheet_name='Data')
            excel_data = output.getvalue()
            
            st.download_button(
                label="📥 Download Excel",
                data=excel_data,
                file_name=f"{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"excel_download_{key_suffix}"
            )

def render_expandable_table(data: pd.DataFrame, title: str, 
                           expand_column: Optional[str] = None):
    """Render table with expandable rows"""
    st.markdown(f"#### {title}")
    
    if data is None or data.empty:
        st.info("No data available")
        return
    
    for idx, row in data.iterrows():
        with st.expander(f"Row {idx + 1}: {row[expand_column] if expand_column else ''}"):
            st.json(row.to_dict())

# ============================================================================
# ALERT & WARNING COMPONENTS
# ============================================================================

def render_alert_card(title: str, message: str, severity: str = "warning"):
    """Render alert card for warnings and notifications"""
    
    icons = {
        "info": "ℹ️",
        "warning": "⚠️",
        "error": "❌",
        "success": "✅"
    }
    
    colors = {
        "info": "#17becf",
        "warning": "#ffbb00",
        "error": "#E31837",
        "success": "#2ca02c"
    }
    
    st.markdown(f"""
    <div style="
        padding: 1rem;
        border-left: 4px solid {colors.get(severity, '#17becf')};
        background-color: rgba(255,255,255,0.05);
        border-radius: 4px;
        margin: 1rem 0;
    ">
        <h4>{icons.get(severity, 'ℹ️')} {title}</h4>
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def format_number(num: float, decimals: int = 2) -> str:
    """Format number with commas and decimals"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.{decimals}f}M"
    elif num >= 1_000:
        return f"{num/1_000:.{decimals}f}K"
    else:
        return f"{num:,.{decimals}f}"

def calculate_percentile(value: float, values: List[float]) -> int:
    """Calculate percentile rank of a value"""
    if not values:
        return 0
    return int((sum(1 for v in values if v < value) / len(values)) * 100)

def render_data_unavailable(message: str = "No data available for the selected filters"):
    """Render data unavailable message"""
    st.info(f"📊 {message}")
