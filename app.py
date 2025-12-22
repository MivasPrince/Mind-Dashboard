"""
MIND Unified Dashboard - Main Application Entry Point
Fixed to work with new dashboard structure (no render() functions)
"""
import sys
from pathlib import Path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import streamlit as st
from core.auth import check_authentication, logout
from core.rbac import check_page_access, get_accessible_pages
from core.theme import initialize_theme, apply_theme_css, get_logo_path, render_theme_toggle
from core.db import get_bigquery_client, run_query
from core.settings import get_table_ref

st.set_page_config(
    page_title="MIND Unified Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_theme()
apply_theme_css()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None

if not st.session_state.authenticated:
    check_authentication()
else:
    with st.sidebar:
        logo_path = get_logo_path()
        if logo_path:
            st.image(str(logo_path), width=200)
        
        st.title("🎓 MIND Dashboard")
        st.write(f"**User:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.role}")
        
        st.divider()
        render_theme_toggle()
        st.divider()
        
        accessible_pages = get_accessible_pages(st.session_state.role)
        st.subheader("Navigation")
        
        if 'Home' in accessible_pages:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.current_page = 'Home'
                st.rerun()
        
        if 'Student' in accessible_pages:
            if st.button("📚 Student Dashboard", use_container_width=True):
                st.session_state.current_page = 'Student'
                st.rerun()
        
        if 'Faculty' in accessible_pages:
            if st.button("👨‍🏫 Faculty Dashboard", use_container_width=True):
                st.session_state.current_page = 'Faculty'
                st.rerun()
        
        if 'Developer' in accessible_pages:
            if st.button("💻 Developer Dashboard", use_container_width=True):
                st.session_state.current_page = 'Developer'
                st.rerun()
        
        if 'Admin' in accessible_pages:
            if st.button("⚙️ Admin Dashboard", use_container_width=True):
                st.session_state.current_page = 'Admin'
                st.rerun()
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
    
    current_page = st.session_state.current_page
    
    if not check_page_access(st.session_state.role, current_page):
        st.error(f"⛔ Access Denied")
        st.stop()
    
    # EXECUTE PAGES (no render() function - code runs directly)
    if current_page == 'Home':
        st.markdown('<h1 class="main-header">📊 MIND Analytics</h1>', unsafe_allow_html=True)
        st.markdown("### Welcome to MIND Learning Analytics Platform")
        
        client = get_bigquery_client()
        if client:
            st.success("✅ Connection successful")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                q = f"SELECT COUNT(DISTINCT user_id) as c FROM {get_table_ref('user')}"
                df = run_query(q, client)
                if df is not None and not df.empty:
                    st.metric("👥 Users", f"{int(df['c'].iloc[0]):,}")
            
            with col2:
                q = f"SELECT COUNT(*) as c FROM {get_table_ref('casestudy')}"
                df = run_query(q, client)
                if df is not None and not df.empty:
                    st.metric("📚 Cases", f"{int(df['c'].iloc[0]):,}")
            
            with col3:
                q = f"SELECT COUNT(*) as c FROM {get_table_ref('sessions')}"
                df = run_query(q, client)
                if df is not None and not df.empty:
                    st.metric("🎯 Sessions", f"{int(df['c'].iloc[0]):,}")
            
            with col4:
                q = f"SELECT COUNT(*) as c FROM {get_table_ref('grades')}"
                df = run_query(q, client)
                if df is not None and not df.empty:
                    st.metric("✅ Grades", f"{int(df['c'].iloc[0]):,}")
        else:
            st.error("❌ Failed to connect")
    
    elif current_page == 'Student':
        exec(open('pages/student.py').read())
    
    elif current_page == 'Faculty':
        exec(open('pages/faculty.py').read())
    
    elif current_page == 'Developer':
        exec(open('pages/developer.py').read())
    
    elif current_page == 'Admin':
        exec(open('pages/admin.py').read())
