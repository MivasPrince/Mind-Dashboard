"""
Student Dashboard - Personalized View
Personal progress, performance trends, benchmarking, and feedback
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from core.db import get_bigquery_client, run_query
from core.settings import get_table_ref
from components.ui import (
    render_kpi_row, render_line_chart, render_bar_chart, render_radar_chart,
    render_data_table, render_gauge_chart, render_data_unavailable
)

def render():
    """Render the enhanced student dashboard page"""
    
    st.markdown('<h1 class="main-header">📚 Student Dashboard</h1>', unsafe_allow_html=True)
    st.write(f"Welcome, **{st.session_state.username}** - Your personal learning analytics")
    
    # Get BigQuery client
    client = get_bigquery_client()
    if client is None:
        st.error("Failed to connect to BigQuery")
        st.stop()
    
    # Student Selector
    st.subheader("👤 Select Student")
    
    users_query = f"""
    SELECT user_id, name, email
    FROM {get_table_ref('user')}
    WHERE role = 'student' OR role IS NULL
    ORDER BY name
    LIMIT 100
    """
    users_df = run_query(users_query, client)
    
    if users_df is None or users_df.empty:
        st.warning("No students found")
        st.stop()
    
    student_options = {f"{row['name']} ({row['email']})": row['user_id'] 
                      for _, row in users_df.iterrows()}
    
    selected_student = st.selectbox(
        "Choose a student",
        options=list(student_options.keys()),
        key="student_selector"
    )
    
    student_id = student_options[selected_student]
    
    st.divider()
    
    # KPI CARDS
    st.subheader("📊 Your Performance Summary")
    
    with st.spinner("Loading metrics..."):
        # Cases Attempted
        attempted_query = f"""
        SELECT COUNT(DISTINCT case_study) as attempted
        FROM {get_table_ref('grades')}
        WHERE user = '{student_id}'
        """
        attempted_df = run_query(attempted_query, client)
        cases_attempted = attempted_df['attempted'].iloc[0] if attempted_df is not None and not attempted_df.empty else 0
        
        # Average Score
        avg_score_query = f"""
        SELECT AVG(final_score) as avg_score
        FROM {get_table_ref('grades')}
        WHERE user = '{student_id}'
        """
        avg_score_df = run_query(avg_score_query, client)
        avg_score = avg_score_df['avg_score'].iloc[0] if avg_score_df is not None and not avg_score_df.empty else 0
    
    render_kpi_row([
        {'title': 'Cases Attempted', 'value': f"{cases_attempted}", 'icon': '📚'},
        {'title': 'Average Score', 'value': f"{avg_score:.1f}", 'icon': '📈'}
    ])
    
    st.divider()
    
    # PERFORMANCE TREND
    st.subheader("📈 Performance Trend")
    
    perf_query = f"""
    SELECT 
        DATE(timestamp) as date,
        AVG(final_score) as avg_score
    FROM {get_table_ref('grades')}
    WHERE user = '{student_id}'
    GROUP BY DATE(timestamp)
    ORDER BY date
    """
    perf_data = run_query(perf_query, client)
    
    if perf_data is not None and not perf_data.empty:
        render_line_chart(perf_data, 'date', 'avg_score', 'Your Progress Over Time')
    else:
        render_data_unavailable()
    
    st.divider()
    
    # RUBRIC SCORES
    st.subheader("🎯 Skills Breakdown")
    
    rubric_query = f"""
    SELECT 
        AVG(individual_scores.communication) as communication,
        AVG(individual_scores.comprehension) as comprehension,
        AVG(individual_scores.critical_thinking) as critical_thinking
    FROM {get_table_ref('grades')}
    WHERE user = '{student_id}'
    """
    rubric_data = run_query(rubric_query, client)
    
    if rubric_data is not None and not rubric_data.empty:
        comm = float(rubric_data['communication'].iloc[0] or 0)
        comp = float(rubric_data['comprehension'].iloc[0] or 0)
        crit = float(rubric_data['critical_thinking'].iloc[0] or 0)
        
        render_radar_chart(
            ['Communication', 'Comprehension', 'Critical Thinking'],
            [comm, comp, crit],
            'Your Rubric Scores'
        )
    else:
        render_data_unavailable()
    
    st.divider()
    
    # RECENT GRADES TABLE
    st.subheader("💬 Recent Feedback")
    
    recent_query = f"""
    SELECT 
        c.title as case_study,
        g.final_score,
        g.overall_summary,
        g.timestamp
    FROM {get_table_ref('grades')} g
    LEFT JOIN {get_table_ref('casestudy')} c ON g.case_study = c.case_study_id
    WHERE g.user = '{student_id}'
    ORDER BY g.timestamp DESC
    LIMIT 10
    """
    recent_data = run_query(recent_query, client)
    
    if recent_data is not None and not recent_data.empty:
        render_data_table(recent_data, "Recent Grades", max_rows=10, key_suffix="recent")
    else:
        render_data_unavailable()

if __name__ == "__main__":
    render()
