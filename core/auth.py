import streamlit as st
import re
from typing import Tuple, Optional, Dict, List
import bcrypt # 1. Import bcrypt
import json

# --- Configuration Constants ---
# Define keys expected within each user's secret section
USER_KEYS = ["username", "password_hash", "role"]

# --- Utility Functions for Secret Loading ---

def _load_user_data() -> List[Dict[str, str]]:
    """
    Reads all user sections from st.secrets that contain the required keys.
    
    Returns:
        A list of dictionaries, where each dict is a user object (username, hash, role).
    """
    user_list = []
    # st.secrets is a Dict-like object. We iterate over its top-level keys.
    for key, config in st.secrets.items():
        # Identify user sections by checking for the 'username' key (or any other required key)
        if isinstance(config, dict) and "username" in config:
            is_valid_user = True
            user_data = {}
            for k in USER_KEYS:
                if k not in config:
                    is_valid_user = False
                    break
                user_data[k] = config[k]
            
            if is_valid_user:
                # Add the user data only if all required keys are present
                user_list.append(user_data)
                
    if not user_list:
        st.error("❌ Authentication Error: No valid user configuration sections found in `secrets.toml`. Check structure (e.g., [admin_user], [faculty_user]).")
        st.stop()
        
    return user_list


@st.cache_data(show_spinner=False)
def get_user_data_map() -> Dict[str, Dict[str, str]]:
    """Caches and returns a map of username -> user_data for quick lookup."""
    user_list = _load_user_data()
    return {user['username'].lower(): user for user in user_list}


# ----------------------------------------------------------------
# --- AUTHENTICATION FUNCTIONS (UPDATED FOR HASHES) ---
# ----------------------------------------------------------------

def get_user_role(username: str) -> Optional[Dict[str, str]]:
    """
    Finds the user's data (including hash and role) by username.
    """
    user_map = get_user_data_map()
    norm_username = username.lower()
    
    # If the user is found, return the full user dictionary
    return user_map.get(norm_username)


def login_widget():
    """Shows the login UI and validates credentials using bcrypt."""
    st.title("🔐 Login to MIND Unified Dashboard")

    username = st.text_input("Username (e.g., admin@example.com)")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            user_data = get_user_role(username)

            if user_data:
                stored_hash = user_data["password_hash"].encode('utf-8')
                input_password = password.encode('utf-8')

                try:
                    # 2. Use bcrypt.checkpw to securely verify the password
                    if bcrypt.checkpw(input_password, stored_hash):
                        authenticate(user_data["username"], user_data["role"])
                    else:
                        st.error("Invalid username or password.")
                except ValueError:
                    # Catch error if the stored hash is malformed
                    st.error("Authentication system error. Contact support.")
            else:
                st.error("Invalid username or password.")
        else:
            st.error("Please enter both username and password.")


def authenticate(username: str, user_role: str):
    """
    Sets session state after successful login.
    """
    st.session_state["authenticated"] = True
    st.session_state["username"] = username
    st.session_state["role"] = user_role

    st.success(f"Login successful ✔ Role: **{user_role}**")
    st.rerun()


def check_authentication() -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Returns the current authentication state and user details.
    """

    # Initialize session state keys if they don't exist
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["role"] = None
        st.session_state["username"] = None


    is_auth = st.session_state["authenticated"]
    role = st.session_state["role"]
    username = st.session_state["username"]

    return is_auth, role, username


def logout_button():
    """Adds a logout button to the sidebar."""
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()


def role_guard(required_role: str) -> Tuple[str, str]:
    """
    Ensures the logged-in user has the correct role for this page.
    Admin has access to all pages.
    """

    is_auth, user_role, username = check_authentication()

    # 1. Check if authenticated
    if not is_auth or user_role is None or username is None:
        st.error("You must log in to access this page.")
        # Stop execution of the rest of the Streamlit page script
        st.stop() 

    # 2. Check Role Authorization
    if user_role != required_role and user_role != "Admin":
        st.error(f"⛔ Access Denied — Only **{required_role}** or **Admin** users can view this page. Your role is **{user_role}**.")
        st.stop()

    return user_role, username
