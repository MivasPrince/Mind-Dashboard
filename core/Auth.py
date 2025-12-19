"""
Authentication module for MIND Dashboard
Handles login/logout with bcrypt password hashing
"""

import streamlit as st
import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a bcrypt hash
    
    Args:
        plain_password: Plain text password
        hashed_password: Bcrypt hashed password
    
    Returns:
        True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

def authenticate_user(username: str, password: str) -> tuple:
    """
    Authenticate user against credentials in Streamlit secrets
    
    Args:
        username: Username to authenticate
        password: Plain text password
    
    Returns:
        Tuple of (success: bool, role: str or None)
    """
    try:
        # Check if secrets are configured
        if 'users' not in st.secrets:
            st.error("⚠️ Authentication not configured. Please contact administrator.")
            return False, None
        
        users = st.secrets['users']
        
        # Check if user exists
        if username not in users:
            return False, None
        
        user_data = users[username]
        
        # Verify password
        if verify_password(password, user_data['password_hash']):
            return True, user_data['role']
        
        return False, None
    
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return False, None

def check_authentication():
    """
    Display login form and handle authentication
    """
    st.title("🎓 MIND Unified Dashboard")
    st.subheader("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                success, role = authenticate_user(username, password)
                
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.role = role
                    st.success(f"✅ Login successful! Welcome, {username}")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
    
    # Help text
    st.info("""
    **Demo Credentials** (if configured):
    - Admin: admin / admin123
    - Faculty: faculty / faculty123
    - Developer: developer / dev123
    - Student: student / student123
    """)

def logout():
    """
    Clear session state and log out user
    """
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.current_page = 'Home'
    st.success("✅ Logged out successfully")
