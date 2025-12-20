"""
Core package for MIND Dashboard
Contains authentication, database, RBAC, theme management, and configuration modules
"""

from core.auth import authenticate_user, check_authentication, logout
from core.db import get_bigquery_client, run_query, test_connection
from core.rbac import check_page_access, get_accessible_pages
from core.settings import get_table_ref, TABLES, BIGQUERY_CONFIG
from core.theme import (
    initialize_theme, toggle_theme, get_current_theme,
    get_logo_path, apply_theme_css, render_theme_toggle, get_theme_colors
)

__all__ = [
    'authenticate_user',
    'check_authentication', 
    'logout',
    'get_bigquery_client',
    'run_query',
    'test_connection',
    'check_page_access',
    'get_accessible_pages',
    'get_table_ref',
    'TABLES',
    'BIGQUERY_CONFIG',
    'initialize_theme',
    'toggle_theme',
    'get_current_theme',
    'get_logo_path',
    'apply_theme_css',
    'render_theme_toggle',
    'get_theme_colors'
]
