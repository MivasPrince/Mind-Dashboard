"""
Student Dashboard Page
Personal learning analytics and performance metrics
"""

import streamlit as st
from core.db import get_bigquery_client, run_query
from core.settings import get_table_ref
from components.ui import (
    render_kpi_row, render_bar_chart, render_line_chart, 
    render_data_table, render_data_unavailable
)
import pandas as pd

def render():
    """Render the student dashboard page"""
    
    st.markdown('<h1 class="main-header">📚 Student Dashboard</h1>', unsafe_allow_html=True)
    st.write(f"Welcome, **{st.session_state.username}**")
    
    # Get BigQuery client
    client = get_bigquery_client()
    if client is None:
        st.error("Failed to connect to BigQuery")
        st.stop()
    
    # Student selector (for demo - in production, this would be the logged-in user)
    st.subheader("👤 Select Student")
    
    users_query = f"""
    SELECT user_id, name, student_email, cohort
    FROM {get_table_ref('user')}
    WHERE role = 'student' OR role IS NULL
    ORDER BY name
    """
    users_df = run_query(users_query, client)
    
    if users_df is None or users_df.empty:
        st.warning("No students found in database")
        st.stop()
    
    # Student selector
    student_options = {f"{row['name']} ({row['student_email']})": row['user_id'] 
                      for _, row in users_df.iterrows()}
    
    selected_student = st.selectbox(
        "Choose a student",
        options=list(student_options.keys()),
        key="student_selector"
    )
    
    student_id = student_options[selected_student]
    
    st.divider()
    
    # Student Overview KPIs
    st.subheader("📊 Your Performance Overview")
    
    with st.spinner("Loading your metrics..."):
        # Total attempts
        attempts_query = f"""
        SELECT COUNT(*) as total_attempts
        FROM {get_table_ref('conversation')}
        WHERE user_id = '{student_id}'
        """
        attempts_df = run_query(attempts_query, client)
        total_attempts = attempts_df['total_attempts'].iloc[0] if attempts_df is not None and not attempts_df.empty else 0
        
        # Average score
        avg_score_query = f"""
        SELECT AVG(final_score) as avg_score
        FROM {get_table_ref('grades')}
        WHERE user_id = '{student_id}'
        """
        avg_score_df = run_query(avg_score_query, client)
        avg_score = avg_score_df['avg_score'].iloc[0] if avg_score_df is not None and not avg_score_df.empty else 0
        
        # Completed cases
        completed_query = f"""
        SELECT COUNT(DISTINCT case_study_id) as completed_cases
        FROM {get_table_ref('grades')}
        WHERE user_id = '{student_id}'
        """
        completed_df = run_query(completed_query, client)
        completed_cases = completed_df['completed_cases'].iloc[0] if completed_df is not None and not completed_df.empty else 0
        
        # Recent activity
        recent_query = f"""
        SELECT MAX(timestamp) as last_activity
        FROM {get_table_ref('conversation')}
        WHERE user_id = '{student_id}'
        """
        recent_df = run_query(recent_query, client)
        last_activity = recent_df['last_activity'].iloc[0] if recent_df is not None and not recent_df.empty else None
    
    # Display KPIs
    render_kpi_row([
        {
            'title': 'Total Attempts',
            'value': f"{total_attempts:,}",
            'icon': '🎯',
            'help_text': 'Total conversation attempts'
        },
        {
            'title': 'Average Score',
            'value': f"{avg_score:.1f}" if avg_score else "N/A",
            'icon': '⭐',
            'help_text': 'Average final score across all graded attempts'
        },
        {
            'title': 'Cases Completed',
            'value': f"{completed_cases:,}",
            'icon': '✅',
            'help_text': 'Number of unique case studies completed'
        },
        {
            'title': 'Last Activity',
            'value': str(last_activity.date()) if last_activity else "Never",
            'icon': '🕒',
            'help_text': 'Most recent learning activity'
        }
    ])
    
    st.divider()
    
    # Performance by Case Study
    st.subheader("📈 Performance by Case Study")
    
    case_performance_query = f"""
    SELECT 
        c.title as case_title,
        COUNT(g.grade_id) as attempts,
        AVG(g.final_score) as avg_score,
        MAX(g.final_score) as best_score,
        AVG(g.communication) as avg_communication,
        AVG(g.comprehension) as avg_comprehension,
        AVG(g.critical_thinking) as avg_critical_thinking
    FROM {get_table_ref('grades')} g
    LEFT JOIN {get_table_ref('casestudy')} c ON g.case_study_id = c.case_study_id
    WHERE g.user_id = '{student_id}'
    GROUP BY c.title
    ORDER BY avg_score DESC
    """
    case_performance = run_query(case_performance_query, client)
    
    if case_performance is not None and not case_performance.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            render_bar_chart(
                case_performance,
                x='case_title',
                y='avg_score',
                title='Average Score by Case Study'
            )
        
        with col2:
            render_bar_chart(
                case_performance,
                x='case_title',
                y='attempts',
                title='Number of Attempts by Case Study'
            )
        
        # Detailed table
        st.markdown("**Detailed Performance Breakdown**")
        render_data_table(case_performance, max_rows=50)
    else:
        render_data_unavailable("grades")
    
    st.divider()
    
    # Rubric Scores Over Time
    st.subheader("📊 Skill Development Over Time")
    
    rubric_timeline_query = f"""
    SELECT 
        DATE(g.timestamp) as date,
        AVG(g.communication) as communication,
        AVG(g.comprehension) as comprehension,
        AVG(g.critical_thinking) as critical_thinking,
        AVG(g.final_score) as overall
    FROM {get_table_ref('grades')} g
    WHERE g.user_id = '{student_id}'
    GROUP BY DATE(g.timestamp)
    ORDER BY date
    """
    rubric_timeline = run_query(rubric_timeline_query, client)
    
    if rubric_timeline is not None and not rubric_timeline.empty:
        # Reshape for line chart
        timeline_long = rubric_timeline.melt(
            id_vars=['date'],
            value_vars=['communication', 'comprehension', 'critical_thinking', 'overall'],
            var_name='skill',
            value_name='score'
        )
        
        render_line_chart(
            timeline_long,
            x='date',
            y='score',
            title='Skill Scores Over Time',
            color='skill'
        )
    else:
        st.info("Not enough data to show skill development timeline")
    
    st.divider()
    
    # Recent Attempts Detail
    st.subheader("🔍 Recent Attempt Details")
    
    recent_attempts_query = f"""
    SELECT 
        c.title as case_title,
        g.attempt,
        g.communication,
        g.comprehension,
        g.critical_thinking,
        g.final_score,
        g.performance_summary,
        g.timestamp
    FROM {get_table_ref('grades')} g
    LEFT JOIN {get_table_ref('casestudy')} c ON g.case_study_id = c.case_study_id
    WHERE g.user_id = '{student_id}'
    ORDER BY g.timestamp DESC
    LIMIT 20
    """
    recent_attempts = run_query(recent_attempts_query, client)
    
    if recent_attempts is not None and not recent_attempts.empty:
        # Display with expandable feedback
        for _, row in recent_attempts.iterrows():
            with st.expander(f"**{row['case_title']}** - Attempt {row['attempt']} | Score: {row['final_score']:.1f} | {row['timestamp']}"):
                cols = st.columns(3)
                cols[0].metric("Communication", f"{row['communication']:.1f}")
                cols[1].metric("Comprehension", f"{row['comprehension']:.1f}")
                cols[2].metric("Critical Thinking", f"{row['critical_thinking']:.1f}")
                
                if row['performance_summary']:
                    st.markdown("**Feedback:**")
                    st.write(row['performance_summary'])
    else:
        st.info("No graded attempts found")
