"""
Configuration and settings for MIND Dashboard
Includes BigQuery connection details and table/field mappings
"""

import streamlit as st

# BigQuery Configuration
BIGQUERY_CONFIG = {
    'project_id': 'gen-lang-client-0625543859',
    'dataset': 'mind_analytics',
    'location': 'europe-west3'  # Updated from EU to actual location
}

# Full table reference helper
def get_table_ref(table_name):
    """Returns fully qualified BigQuery table reference"""
    return f"`{BIGQUERY_CONFIG['project_id']}.{BIGQUERY_CONFIG['dataset']}.{table_name}`"

# Table mappings with display names and descriptions
TABLES = {
    'user': {
        'name': 'user',
        'display_name': 'Users',
        'description': 'Platform users (students, instructors, admins)',
        'primary_key': 'user_id'
    },
    'casestudy': {
        'name': 'casestudy',
        'display_name': 'Case Studies',
        'description': 'Learning scenarios and cases',
        'primary_key': 'case_study_id'
    },
    'case_study_avatar': {
        'name': 'case_study_avatar',
        'display_name': 'Case Study Avatars',
        'description': 'Personas used in case studies',
        'primary_key': 'avatar_id'
    },
    'sessions': {
        'name': 'sessions',
        'display_name': 'Sessions',
        'description': 'User engagement sessions',
        'primary_key': 'session_pk'
    },
    'conversation': {
        'name': 'conversation',
        'display_name': 'Conversations',
        'description': 'AI-learner interactions',
        'primary_key': 'conversation_id'
    },
    'grades': {
        'name': 'grades',
        'display_name': 'Grades',
        'description': 'Rubric-based evaluations',
        'primary_key': 'grade_id'
    },
    'session_analytics': {
        'name': 'session_analytics',
        'display_name': 'Session Analytics',
        'description': 'PostHog session data',
        'primary_key': 'session_id'
    },
    'event_stream': {
        'name': 'event_stream',
        'display_name': 'Event Stream',
        'description': 'PostHog event-level data',
        'primary_key': 'event_id'
    },
    'backend_telemetry': {
        'name': 'backend_telemetry',
        'display_name': 'Backend Telemetry',
        'description': 'Backend and AI observability data',
        'primary_key': 'telemetry_id'
    }
}

# Field mappings for each table
FIELD_MAPPINGS = {
    'user': {
        'user_id': {'display': 'User ID', 'required': True},
        'name': {'display': 'Name', 'required': True},
        'email': {'display': 'Email', 'required': True},  # Changed from student_email
        'role': {'display': 'Role', 'required': False},
        'department': {'display': 'Department', 'required': False},
        'cohort': {'display': 'Cohort', 'required': False},
        'posthog_distinct_email': {'display': 'PostHog Email', 'required': False},  # Changed from posthog_distinct_id
        'date_added': {'display': 'Date Added', 'required': False},
        'date_updated': {'display': 'Date Updated', 'required': False}
    },
    'grades': {
        'grade_id': {'display': 'Grade ID', 'required': True},
        'conversation_id': {'display': 'Conversation ID', 'required': False},
        'case_study_id': {'display': 'Case Study ID', 'required': False},
        'user_id': {'display': 'User ID', 'required': False},
        'attempt': {'display': 'Attempt', 'required': False},
        'communication': {'display': 'Communication', 'required': False},
        'comprehension': {'display': 'Comprehension', 'required': False},
        'critical_thinking': {'display': 'Critical Thinking', 'required': False},
        'final_score': {'display': 'Final Score', 'required': False},
        'performance_summary': {'display': 'Performance Summary', 'required': False},
        'overall_summary': {'display': 'Overall Summary', 'required': False},
        'timestamp': {'display': 'Timestamp', 'required': False}
    },
    'casestudy': {
        'case_study_id': {'display': 'Case Study ID', 'required': True},
        'agent_id': {'display': 'Agent ID', 'required': False},
        'title': {'display': 'Title', 'required': True},
        'description': {'display': 'Description', 'required': False},
        'avatar_id': {'display': 'Avatar ID', 'required': False}
    },
    'sessions': {
        '_id': {'display': 'User ID', 'required': True},  # Changed from session_pk and user_id
        'case_study_id': {'display': 'Case Study ID', 'required': False},
        'user_email': {'display': 'User Email', 'required': False},
        'start_time': {'display': 'Start Time', 'required': False},
        'end_time': {'display': 'End Time', 'required': False},
        'last_activity': {'display': 'Last Activity', 'required': False},
        'is_active': {'display': 'Is Active', 'required': False},
        'transcript': {'display': 'Transcript', 'required': False}
    },
    'conversation': {
        'conversation_id': {'display': 'Conversation ID', 'required': True},
        'case_study_id': {'display': 'Case Study ID', 'required': False},
        'user_id': {'display': 'User ID', 'required': False},
        'session_attempt': {'display': 'Session Attempt', 'required': False},
        'timestamp': {'display': 'Timestamp', 'required': False},
        'transcript': {'display': 'Transcript', 'required': False},
        'request_id': {'display': 'Request ID', 'required': False}
    },
    'session_analytics': {
        'session_id': {'display': 'Session ID', 'required': True},
        'distinct_id': {'display': 'Distinct ID', 'required': True},
        'derived_session_length_minutes': {'display': 'Session Length (min)', 'required': False},
        'derived_engagement_score': {'display': 'Engagement Score', 'required': False},
        'derived_session_type': {'display': 'Session Type', 'required': False},
        'pageview_count': {'display': 'Pageviews', 'required': False},
        'is_bounce': {'display': 'Is Bounce', 'required': False}
    },
    'backend_telemetry': {
        'telemetry_id': {'display': 'Telemetry ID', 'required': True},
        'derived_response_time_ms': {'display': 'Response Time (ms)', 'required': False},
        'derived_is_error': {'display': 'Is Error', 'required': False},
        'derived_endpoint_group': {'display': 'Endpoint Group', 'required': False},
        'derived_ai_total_tokens': {'display': 'AI Tokens', 'required': False},
        'derived_ai_model': {'display': 'AI Model', 'required': False},
        'http_status_code': {'display': 'HTTP Status', 'required': False}
    }
}

# Color scheme for consistent UI (MIVA branding)
COLORS = {
    'primary': '#E31837',       # MIVA Red - primary brand color
    'secondary': '#262730',     # Dark gray - works in both light and dark modes
    'success': '#2ca02c',       # Green - for positive metrics
    'warning': '#ffbb00',       # Amber - for caution/attention
    'danger': '#E31837',        # MIVA Red - for errors (using brand color)
    'info': '#17becf',          # Cyan - for informational content
    'light_bg': '#FFFFFF',      # White - light mode background
    'light_secondary': '#F0F2F6',  # Light gray - light mode secondary
    'dark_bg': '#0E1117',       # Deep black - dark mode background
    'dark_secondary': '#262730', # Dark gray - dark mode secondary
    'light_text': '#262730',    # Dark gray - light mode text
    'dark_text': '#FAFAFA'      # Very light gray - dark mode text
}

# Dashboard refresh intervals (in seconds)
REFRESH_INTERVALS = {
    'realtime': 30,
    'standard': 300,
    'batch': 3600
}
