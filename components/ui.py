"""
Reusable UI components for dashboards
Includes KPI cards, filters, charts, and data tables
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional
from core.settings import COLORS

def render_kpi_card(title: str, value: any, delta: Optional[str] = None, 
                   help_text: Optional[str] = None, icon: str = "📊"):
    """
    Render a KPI metric card
    
    Args:
        title: KPI title
        value: KPI value
        delta: Optional delta/change indicator
        help_text: Optional help text
        icon: Optional emoji icon
    """
    with st.container():
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown(f"<h1>{icon}</h1>", unsafe_allow_html=True)
        with col2:
            if delta:
                st.metric(
                    label=title,
                    value=value,
                    delta=delta,
                    help=help_text
                )
            else:
                st.metric(
                    label=title,
                    value=value,
                    help=help_text
                )

def render_kpi_row(kpis: list):
    """
    Render a row of KPI cards
    
    Args:
        kpis: List of dicts with keys: title, value, delta (optional), help_text (optional), icon (optional)
    """
    cols = st.columns(len(kpis))
    
    for col, kpi in zip(cols, kpis):
        with col:
            render_kpi_card(
                title=kpi['title'],
                value=kpi['value'],
                delta=kpi.get('delta'),
                help_text=kpi.get('help_text'),
                icon=kpi.get('icon', '📊')
            )

def render_date_filter(key: str = "date_filter") -> tuple:
    """
    Render date range filter
    
    Args:
        key: Unique key for the filter
    
    Returns:
        Tuple of (start_date, end_date)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            key=f"{key}_start",
            value=pd.Timestamp.now() - pd.Timedelta(days=30)
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            key=f"{key}_end",
            value=pd.Timestamp.now()
        )
    
    return start_date, end_date

def render_bar_chart(df: pd.DataFrame, x: str, y: str, title: str, 
                    color: Optional[str] = None, horizontal: bool = False):
    """
    Render a bar chart using Plotly
    
    Args:
        df: DataFrame with data
        x: Column for x-axis
        y: Column for y-axis
        title: Chart title
        color: Optional column for color grouping
        horizontal: If True, render horizontal bar chart
    """
    if df is None or df.empty:
        st.info("No data available for chart")
        return
    
    if horizontal:
        fig = px.bar(
            df, 
            y=x, 
            x=y, 
            title=title,
            color=color,
            orientation='h'
        )
    else:
        fig = px.bar(
            df, 
            x=x, 
            y=y, 
            title=title,
            color=color
        )
    
    fig.update_layout(
        template="plotly_white",
        height=400,
        showlegend=True if color else False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_line_chart(df: pd.DataFrame, x: str, y: str, title: str, 
                     color: Optional[str] = None):
    """
    Render a line chart using Plotly
    
    Args:
        df: DataFrame with data
        x: Column for x-axis
        y: Column for y-axis
        title: Chart title
        color: Optional column for color grouping
    """
    if df is None or df.empty:
        st.info("No data available for chart")
        return
    
    fig = px.line(
        df, 
        x=x, 
        y=y, 
        title=title,
        color=color,
        markers=True
    )
    
    fig.update_layout(
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_pie_chart(df: pd.DataFrame, names: str, values: str, title: str):
    """
    Render a pie chart using Plotly
    
    Args:
        df: DataFrame with data
        names: Column for slice names
        values: Column for slice values
        title: Chart title
    """
    if df is None or df.empty:
        st.info("No data available for chart")
        return
    
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title
    )
    
    fig.update_layout(
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_heatmap(df: pd.DataFrame, x: str, y: str, z: str, title: str):
    """
    Render a heatmap using Plotly
    
    Args:
        df: DataFrame with data
        x: Column for x-axis
        y: Column for y-axis
        z: Column for values
        title: Chart title
    """
    if df is None or df.empty:
        st.info("No data available for heatmap")
        return
    
    # Pivot data for heatmap
    pivot_df = df.pivot_table(index=y, columns=x, values=z, aggfunc='mean')
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='RdYlGn',
        text=pivot_df.values,
        texttemplate='%{text:.1f}',
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        title=title,
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_data_table(df: pd.DataFrame, title: Optional[str] = None, 
                     max_rows: int = 100, download: bool = True):
    """
    Render a data table with optional download
    
    Args:
        df: DataFrame to display
        title: Optional table title
        max_rows: Maximum rows to display
        download: Enable CSV download button
    """
    if df is None or df.empty:
        st.info("No data available")
        return
    
    if title:
        st.subheader(title)
    
    # Display row count
    st.caption(f"Showing {min(len(df), max_rows)} of {len(df)} rows")
    
    # Display table
    st.dataframe(
        df.head(max_rows),
        use_container_width=True,
        height=400
    )
    
    # Download button
    if download:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{title.lower().replace(' ', '_')}.csv" if title else "data.csv",
            mime="text/csv"
        )

def render_loading_message(message: str = "Loading data..."):
    """
    Display a loading message with spinner
    
    Args:
        message: Loading message text
    """
    with st.spinner(message):
        st.empty()

def render_error_message(message: str, details: Optional[str] = None):
    """
    Display an error message with optional details
    
    Args:
        message: Error message
        details: Optional detailed error information
    """
    st.error(f"❌ {message}")
    
    if details:
        with st.expander("Error Details"):
            st.code(details)

def render_data_unavailable(table_name: str):
    """
    Display a message when data is not available
    
    Args:
        table_name: Name of the unavailable table/data
    """
    st.warning(f"⚠️ Data not available: {table_name}")
    st.info("This chart/table requires data that is not currently available in the database.")
