"""
Home Dashboard Page
Overview and welcome screen
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from core.db import get_bigquery_client, run_query, test_connection
from core.settings import get_table_ref
from components.ui import render_kpi_row, render_data_table
import pandas as pd

def render():
    """Render the home dashboard page"""
    
    st.markdown('<h1 class="main-header">🏠 MIND Unified Dashboard</h1>', unsafe_allow_html=True)
    st.write(f"Welcome, **{st.session_state.username}** ({st.session_state.role})")
    
    # Test connection
    st.subheader("📊 System Status")
    success, message = test_connection()
    
    if success:
        st.success(f"✅ {message}")
    else:
        st.error(f"❌ {message}")
        st.stop()
    
    # Get BigQuery client
    client = get_bigquery_client()
    
    if client is None:
        st.error("Failed to connect to BigQuery")
        st.stop()
    
    # Platform Overview KPIs
    st.subheader("📈 Platform Overview")
    
    with st.spinner("Loading platform metrics..."):
        # Total users
        users_query = f"SELECT COUNT(*) as total_users FROM {get_table_ref('user')}"
        users_df = run_query(users_query, client)
        total_users = users_df['total_users'].iloc[0] if users_df is not None and not users_df.empty else 0
        
        # Total case studies
        cases_query = f"SELECT COUNT(*) as total_cases FROM {get_table_ref('casestudy')}"
        cases_df = run_query(cases_query, client)
        total_cases = cases_df['total_cases'].iloc[0] if cases_df is not None and not cases_df.empty else 0
        
        # Total sessions
        sessions_query = f"SELECT COUNT(*) as total_sessions FROM {get_table_ref('sessions')}"
        sessions_df = run_query(sessions_query, client)
        total_sessions = sessions_df['total_sessions'].iloc[0] if sessions_df is not None and not sessions_df.empty else 0
        
        # Total grades
        grades_query = f"SELECT COUNT(*) as total_grades FROM {get_table_ref('grades')}"
        grades_df = run_query(grades_query, client)
        total_grades = grades_df['total_grades'].iloc[0] if grades_df is not None and not grades_df.empty else 0
    
    # Display KPIs
    render_kpi_row([
        {
            'title': 'Total Users',
            'value': f"{total_users:,}",
            'icon': '👥',
            'help_text': 'Total registered users'
        },
        {
            'title': 'Case Studies',
            'value': f"{total_cases:,}",
            'icon': '📚',
            'help_text': 'Available learning scenarios'
        },
        {
            'title': 'Learning Sessions',
            'value': f"{total_sessions:,}",
            'icon': '🎯',
            'help_text': 'Total engagement sessions'
        },
        {
            'title': 'Graded Attempts',
            'value': f"{total_grades:,}",
            'icon': '✅',
            'help_text': 'Total graded conversations'
        }
    ])
    
    st.divider()
    
    # Recent Activity
    st.subheader("🕒 Recent Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Recent Sessions**")
        recent_sessions_query = f"""
        SELECT 
            s.session_pk,
            u.name as user_name,
            c.title as case_title,
            s.start_time,
            s.is_active
        FROM {get_table_ref('sessions')} s
        LEFT JOIN {get_table_ref('user')} u ON s.user_id = u.user_id
        LEFT JOIN {get_table_ref('casestudy')} c ON s.case_study_id = c.case_study_id
        ORDER BY s.start_time DESC
        LIMIT 10
        """
        recent_sessions = run_query(recent_sessions_query, client)
        
        if recent_sessions is not None and not recent_sessions.empty:
            display_sessions = recent_sessions[['user_name', 'case_title', 'start_time', 'is_active']]
            display_sessions.columns = ['User', 'Case Study', 'Started', 'Active']
            st.dataframe(display_sessions, use_container_width=True, hide_index=True)
        else:
            st.info("No recent sessions")
    
    with col2:
        st.markdown("**Recent Grades**")
        recent_grades_query = f"""
        SELECT 
            u.name as user_name,
            c.title as case_title,
            g.final_score,
            g.timestamp
        FROM {get_table_ref('grades')} g
        LEFT JOIN {get_table_ref('user')} u ON g.user_id = u.user_id
        LEFT JOIN {get_table_ref('casestudy')} c ON g.case_study_id = c.case_study_id
        ORDER BY g.timestamp DESC
        LIMIT 10
        """
        recent_grades = run_query(recent_grades_query, client)
        
        if recent_grades is not None and not recent_grades.empty:
            display_grades = recent_grades[['user_name', 'case_title', 'final_score', 'timestamp']]
            display_grades.columns = ['User', 'Case Study', 'Score', 'Time']
            st.dataframe(display_grades, use_container_width=True, hide_index=True)
        else:
            st.info("No recent grades")
    
    st.divider()
    
    # Role-specific guidance
    st.subheader("🧭 Quick Navigation")
    
    role = st.session_state.role
    
    if role == 'Student':
        st.info("""
        **Student Dashboard** - View your personal learning analytics:
        - Your performance metrics and progress
        - Case study attempts and scores
        - Recent activity timeline
        """)
    
    elif role == 'Faculty':
        st.info("""
        **Faculty Dashboard** - Monitor student performance:
        - Cohort-level analytics
        - Individual student insights
        - At-risk student detection
        - Rubric score distributions
        """)
    
    elif role == 'Developer':
        st.info("""
        **Developer Dashboard** - System monitoring and data quality:
        - Data freshness checks
        - Pipeline health indicators
        - Error tracking and anomaly detection
        """)
    
    elif role == 'Admin':
        st.info("""
        **Admin Dashboard** - Organization-wide insights:
        - Platform adoption metrics
        - User engagement analytics
        - System usage and trends
        - Access to all dashboards
        """)
