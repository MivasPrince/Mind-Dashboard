"""
MIND Unified Dashboard - Main Application Entry Point
Streamlit multi-page app with RBAC and BigQuery backend
"""

import streamlit as st
from core.auth import check_authentication, logout
from core.rbac import check_page_access, get_accessible_pages

# Page configuration
st.set_page_config(
    page_title="MIND Unified Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None

# Authentication check
if not st.session_state.authenticated:
    check_authentication()
else:
    # Sidebar navigation
    with st.sidebar:
        st.title("🎓 MIND Dashboard")
        st.write(f"**User:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.role}")
        st.divider()
        
        # Get accessible pages for current user
        accessible_pages = get_accessible_pages(st.session_state.role)
        
        st.subheader("Navigation")
        
        # Create navigation buttons
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
    
    # Initialize current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
    
    # Page routing
    current_page = st.session_state.current_page
    
    # Check access
    if not check_page_access(st.session_state.role, current_page):
        st.error(f"⛔ Access Denied: You don't have permission to view the {current_page} page.")
        st.info("Please navigate to an accessible page from the sidebar.")
        st.stop()
    
    # Import and render the appropriate page
    if current_page == 'Home':
        from pages import home
        home.render()
    elif current_page == 'Student':
        from pages import student
        student.render()
    elif current_page == 'Faculty':
        from pages import faculty
        faculty.render()
    elif current_page == 'Developer':
        from pages import developer
        developer.render()
    elif current_page == 'Admin':
        from pages import admin
        admin.render()
