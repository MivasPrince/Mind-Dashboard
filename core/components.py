"""
Reusable UI components for MIND Unified Dashboard
KPI cards, charts, tables, and other visual elements
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any, Optional
from theme import COLORS, CHART_COLORS, get_plotly_theme
from core.utils import format_number, format_percentage, format_duration

def render_kpi_card(title: str, value: Any, delta: Optional[str] = None, 
                    help_text: Optional[str] = None, accent: bool = False):
    """
    Render a KPI card with title, value, and optional delta
    
    Args:
        title: KPI title
        value: KPI value (will be formatted appropriately)
        delta: Change indicator (e.g., "+5.2%" or "↑ 12 students")
        help_text: Tooltip help text
        accent: Use accent border color
    """
    border_color = COLORS['accent'] if accent else COLORS['primary']
    
    st.markdown(f"""
    <div style="
        background-color: {COLORS['white']};
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid {border_color};
        margin-bottom: 10px;
    ">
        <div style="color: {COLORS['text_light']}; font-size: 0.9rem; margin-bottom: 8px;">
            {title}
        </div>
        <div style="color: {COLORS['primary']}; font-size: 2rem; font-weight: 600; margin-bottom: 5px;">
            {value}
        </div>
        {f'<div style="color: {COLORS["success"]}; font-size: 0.85rem;">{delta}</div>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

def render_metric_grid(metrics: List[Dict[str, Any]], columns: int = 4):
    """
    Render a grid of metric cards
    
    Args:
        metrics: List of metric dictionaries with keys: title, value, delta, help_text
        columns: Number of columns in the grid
    """
    cols = st.columns(columns)
    
    for idx, metric in enumerate(metrics):
        with cols[idx % columns]:
            render_kpi_card(
                title=metric.get('title', ''),
                value=metric.get('value', 'N/A'),
                delta=metric.get('delta'),
                help_text=metric.get('help_text'),
                accent=metric.get('accent', False)
            )

def create_line_chart(df: pd.DataFrame, x: str, y: str, title: str,
                      color: Optional[str] = None, 
                      x_label: Optional[str] = None,
                      y_label: Optional[str] = None) -> go.Figure:
    """
    Create a line chart with theme styling
    
    Args:
        df: Data frame
        x: X-axis column name
        y: Y-axis column name
        title: Chart title
        color: Optional column for color grouping
        x_label: X-axis label
        y_label: Y-axis label
        
    Returns:
        Plotly figure
    """
    if df.empty:
        return create_empty_chart("No data available")
    
    fig = px.line(
        df, x=x, y=y, color=color, title=title,
        labels={x: x_label or x, y: y_label or y}
    )
    
    fig.update_layout(**get_plotly_theme()['layout'])
    fig.update_traces(line=dict(width=3))
    
    return fig

def create_bar_chart(df: pd.DataFrame, x: str, y: str, title: str,
                     color: Optional[str] = None,
                     orientation: str = 'v',
                     x_label: Optional[str] = None,
                     y_label: Optional[str] = None) -> go.Figure:
    """
    Create a bar chart with theme styling
    
    Args:
        df: Data frame
        x: X-axis column name
        y: Y-axis column name
        title: Chart title
        color: Optional column for color grouping
        orientation: 'v' for vertical, 'h' for horizontal
        x_label: X-axis label
        y_label: Y-axis label
        
    Returns:
        Plotly figure
    """
    if df.empty:
        return create_empty_chart("No data available")
    
    fig = px.bar(
        df, x=x, y=y, color=color, title=title,
        orientation=orientation,
        labels={x: x_label or x, y: y_label or y}
    )
    
    fig.update_layout(**get_plotly_theme()['layout'])
    
    return fig

def create_scatter_plot(df: pd.DataFrame, x: str, y: str, title: str,
                       color: Optional[str] = None,
                       size: Optional[str] = None,
                       x_label: Optional[str] = None,
                       y_label: Optional[str] = None) -> go.Figure:
    """
    Create a scatter plot with theme styling
    
    Args:
        df: Data frame
        x: X-axis column name
        y: Y-axis column name
        title: Chart title
        color: Optional column for color coding
        size: Optional column for point sizes
        x_label: X-axis label
        y_label: Y-axis label
        
    Returns:
        Plotly figure
    """
    if df.empty:
        return create_empty_chart("No data available")
    
    fig = px.scatter(
        df, x=x, y=y, color=color, size=size, title=title,
        labels={x: x_label or x, y: y_label or y}
    )
    
    fig.update_layout(**get_plotly_theme()['layout'])
    
    return fig

def create_histogram(df: pd.DataFrame, x: str, title: str,
                    nbins: int = 30,
                    x_label: Optional[str] = None) -> go.Figure:
    """
    Create a histogram with theme styling
    
    Args:
        df: Data frame
        x: Column name for histogram
        title: Chart title
        nbins: Number of bins
        x_label: X-axis label
        
    Returns:
        Plotly figure
    """
    if df.empty:
        return create_empty_chart("No data available")
    
    fig = px.histogram(
        df, x=x, title=title, nbins=nbins,
        labels={x: x_label or x}
    )
    
    fig.update_layout(**get_plotly_theme()['layout'])
    fig.update_traces(marker_color=COLORS['primary'])
    
    return fig

def create_box_plot(df: pd.DataFrame, x: str, y: str, title: str,
                   color: Optional[str] = None,
                   x_label: Optional[str] = None,
                   y_label: Optional[str] = None) -> go.Figure:
    """
    Create a box plot with theme styling
    
    Args:
        df: Data frame
        x: X-axis column name (categories)
        y: Y-axis column name (values)
        title: Chart title
        color: Optional column for color grouping
        x_label: X-axis label
        y_label: Y-axis label
        
    Returns:
        Plotly figure
    """
    if df.empty:
        return create_empty_chart("No data available")
    
    fig = px.box(
        df, x=x, y=y, color=color, title=title,
        labels={x: x_label or x, y: y_label or y}
    )
    
    fig.update_layout(**get_plotly_theme()['layout'])
    
    return fig

def create_heatmap(df: pd.DataFrame, title: str,
                   x_label: Optional[str] = None,
                   y_label: Optional[str] = None,
                   colorscale: str = 'RdYlGn') -> go.Figure:
    """
    Create a heatmap with theme styling
    
    Args:
        df: Data frame (already pivoted if needed)
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        colorscale: Color scale name
        
    Returns:
        Plotly figure
    """
    if df.empty:
        return create_empty_chart("No data available")
    
    fig = go.Figure(data=go.Heatmap(
        z=df.values,
        x=df.columns,
        y=df.index,
        colorscale=colorscale,
        text=df.values,
        texttemplate='%{text:.1f}',
        textfont={"size": 10}
    ))
    
    theme_layout = get_plotly_theme()['layout'].copy()
    theme_layout['title'] = title
    if x_label:
        theme_layout['xaxis_title'] = x_label
    if y_label:
        theme_layout['yaxis_title'] = y_label
    
    fig.update_layout(**theme_layout)
    
    return fig

def create_pie_chart(df: pd.DataFrame, names: str, values: str, title: str) -> go.Figure:
    """
    Create a pie chart with theme styling
    
    Args:
        df: Data frame
        names: Column for pie labels
        values: Column for pie values
        title: Chart title
        
    Returns:
        Plotly figure
    """
    if df.empty:
        return create_empty_chart("No data available")
    
    fig = px.pie(df, names=names, values=values, title=title)
    
    fig.update_layout(**get_plotly_theme()['layout'])
    fig.update_traces(
        marker=dict(colors=CHART_COLORS['primary_gradient']),
        textposition='inside',
        textinfo='percent+label'
    )
    
    return fig

def create_empty_chart(message: str = "No data available") -> go.Figure:
    """Create an empty chart with a message"""
    fig = go.Figure()
    
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color=COLORS['text_light'])
    )
    
    fig.update_layout(
        **get_plotly_theme()['layout'],
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
    )
    
    return fig

def render_data_table(df: pd.DataFrame, title: Optional[str] = None, 
                     height: int = 400, key: Optional[str] = None):
    """
    Render a styled data table
    
    Args:
        df: DataFrame to display
        title: Optional table title
        height: Table height in pixels
        key: Unique key for the dataframe widget
    """
    if title:
        st.markdown(f"### {title}")
    
    if df.empty:
        st.info("No data available")
        return
    
    st.dataframe(
        df,
        use_container_width=True,
        height=height,
        key=key
    )

def render_summary_section(title: str, metrics: Dict[str, Any]):
    """
    Render a summary section with key-value pairs
    
    Args:
        title: Section title
        metrics: Dictionary of metric_name: value
    """
    st.markdown(f"### {title}")
    
    for key, value in metrics.items():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**{key}**")
        with col2:
            st.markdown(f"{value}")

def create_gauge_chart(value: float, max_value: float = 100, 
                      title: str = "", suffix: str = "%") -> go.Figure:
    """
    Create a gauge chart for displaying metrics
    
    Args:
        value: Current value
        max_value: Maximum value for the gauge
        title: Chart title
        suffix: Suffix for the value display
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        number={'suffix': suffix},
        gauge={
            'axis': {'range': [0, max_value]},
            'bar': {'color': COLORS['primary']},
            'steps': [
                {'range': [0, max_value * 0.5], 'color': COLORS['danger']},
                {'range': [max_value * 0.5, max_value * 0.75], 'color': COLORS['warning']},
                {'range': [max_value * 0.75, max_value], 'color': COLORS['success']}
            ],
            'threshold': {
                'line': {'color': COLORS['accent'], 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(**get_plotly_theme()['layout'], height=250)
    
    return fig

def render_filter_section():
    """Render a collapsible filter section"""
    with st.expander("🔍 Filters", expanded=False):
        return st.container()

def show_loading_message(message: str = "Loading data..."):
    """Display a loading message with spinner"""
    with st.spinner(message):
        return st.empty()
