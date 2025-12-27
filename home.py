"""
MIND Unified Dashboard - Home Page (CORRECTED)
Proper Streamlit multi-page app entry point
"""

import streamlit as st
from core.auth import check_authentication, logout, is_authenticated
from core.theme import initialize_theme, apply_theme_css, get_logo_path, render_theme_toggle
from core.db import get_bigquery_client, run_query
from core.settings import get_table_ref

# Apply theme first
initialize_theme()

# Page configuration
st.set_page_config(
    page_title="MIND Unified Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply theme CSS
apply_theme_css()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None

# Sidebar
with st.sidebar:
    # Logo
    logo_path = get_logo_path()
    if logo_path:
        st.image(str(logo_path), width=200)
    
    st.title("🎓 MIND Dashboard")
    
    # Theme toggle
    render_theme_toggle()
    
    st.divider()
    
    # Authentication status
    if st.session_state.authenticated:
        st.success(f"👤 **{st.session_state.username}**")
        st.caption(f"Role: {st.session_state.role}")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
    else:
        st.info("Please log in to continue")
    
    st.divider()
    
    # Navigation info
    if st.session_state.authenticated:
        st.markdown("### 📊 Available Dashboards")
        st.markdown("""
        Navigate using the sidebar menu above:
        - 📚 Student Dashboard
        - 👨‍🏫 Faculty Dashboard
        - 💻 Developer Dashboard
        - ⚙️ Admin Dashboard
        """)
        st.caption("Access depends on your role")

# Main content
if not st.session_state.authenticated:
    # Login page
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("# 📊 MIND Analytics Platform")
        st.markdown("---")
        
        st.markdown("""
        ### Centralized Analytics for Learning Excellence
        
        **Platform Features:**
        - 📚 Student Performance Tracking
        - 👨‍🏫 Faculty Cohort Insights
        - 💻 System Health Monitoring
        - ⚙️ Administrative KPIs
        
        Please log in to access your dashboard.
        """)
        
        st.markdown("---")
        
        # Login form
        check_authentication()

else:
    # Home page for authenticated users
    st.markdown(f"# Welcome to MIND Analytics, {st.session_state.username}! 👋")
    st.markdown(f"**Your Role:** {st.session_state.role}")
    st.markdown("---")
    
    # Platform overview
    st.markdown("### 🎯 Platform Overview")
    
    client = get_bigquery_client()
    
    if client:
        st.success("✅ Database Connection Active")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            users_q = f"SELECT COUNT(DISTINCT user_id) as count FROM {get_table_ref('user')}"
            users_df = run_query(users_q, client)
            if users_df is not None and not users_df.empty:
                st.metric("👥 Total Users", f"{int(users_df['count'].iloc[0]):,}")
        
        with col2:
            cases_q = f"SELECT COUNT(*) as count FROM {get_table_ref('casestudy')}"
            cases_df = run_query(cases_q, client)
            if cases_df is not None and not cases_df.empty:
                st.metric("📚 Case Studies", f"{int(cases_df['count'].iloc[0]):,}")
        
        with col3:
            sessions_q = f"SELECT COUNT(*) as count FROM {get_table_ref('sessions')}"
            sessions_df = run_query(sessions_q, client)
            if sessions_df is not None and not sessions_df.empty:
                st.metric("🎯 Learning Sessions", f"{int(sessions_df['count'].iloc[0]):,}")
        
        with col4:
            grades_q = f"SELECT COUNT(*) as count FROM {get_table_ref('grades')}"
            grades_df = run_query(grades_q, client)
            if grades_df is not None and not grades_df.empty:
                st.metric("✅ Graded Attempts", f"{int(grades_df['count'].iloc[0]):,}")
        
        st.markdown("---")
        
        # Role-specific guidance
        st.markdown("### 🧭 Getting Started")
        
        if st.session_state.role == "Admin":
            st.markdown("""
            As an **Administrator**, you have access to all dashboards:
            
            - **📚 Student Dashboard** - Individual learner analytics
            - **👨‍🏫 Faculty Dashboard** - Cohort performance and at-risk identification
            - **💻 Developer Dashboard** - System health and telemetry
            - **⚙️ Admin Dashboard** - Institution-wide KPIs and trends
            
            Use the sidebar to navigate between dashboards.
            """)
        
        elif st.session_state.role == "Faculty":
            st.markdown("""
            As **Faculty**, access your teaching analytics:
            
            - **👨‍🏫 Faculty Dashboard** - Monitor cohort performance, identify at-risk students
            
            Navigate using the sidebar menu above.
            """)
        
        elif st.session_state.role == "Student":
            st.markdown("""
            As a **Student**, track your learning journey:
            
            - **📚 Student Dashboard** - View your performance metrics and progress
            
            Navigate using the sidebar menu above.
            """)
        
        elif st.session_state.role == "Developer":
            st.markdown("""
            As a **Developer**, monitor system health:
            
            - **💻 Developer Dashboard** - System telemetry, errors, and AI usage
            
            Navigate using the sidebar menu above.
            """)
    
    else:
        st.error("❌ Unable to connect to database")
        st.info("Please check your connection settings or contact support.")
    
    st.markdown("---")
    
    # Recent activity
    st.markdown("### 🕒 Recent Platform Activity")
    
    if client:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Latest Sessions")
            sessions_q = f"""
            SELECT start_time, user_email, is_active
            FROM {get_table_ref('sessions')}
            ORDER BY start_time DESC
            LIMIT 5
            """
            recent_sessions = run_query(sessions_q, client)
            if recent_sessions is not None and not recent_sessions.empty:
                st.dataframe(recent_sessions, use_container_width=True, height=200)
        
        with col2:
            st.markdown("#### Latest Grades")
            grades_q = f"""
            SELECT timestamp, final_score
            FROM {get_table_ref('grades')}
            ORDER BY timestamp DESC
            LIMIT 5
            """
            recent_grades = run_query(grades_q, client)
            if recent_grades is not None and not recent_grades.empty:
                st.dataframe(recent_grades, use_container_width=True, height=200)

st.caption("💡 MIND Analytics Platform - Powered by BigQuery & Streamlit")
