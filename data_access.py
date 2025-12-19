"""data_access.py

Centralized, read-only query layer for the dashboard.

All table names below follow the new, standardized (lowercase) naming:
- user
- case_sstudy
- case_study_avatar
- sessions
- conversation
- grades

Telemetry / analytics tables (from Logfire + PostHog exports):
- backend_telemetry
- web_sessions
- web_events
"""

from __future__ import annotations

from typing import Optional

import pandas as pd

from db import get_db_manager


def _tbl(name: str) -> str:
    bq = get_db_manager()
    return bq.config.table(name)


# -----------------------------
# Core domain (case studies)
# -----------------------------

def get_case_studies() -> pd.DataFrame:
    q = f"""
    SELECT
      case_study_id,
      agent_id,
      avatar_id,
      title,
      description,
      created_at,
      updated_at
    FROM {_tbl('case_sstudy')}
    ORDER BY created_at DESC
    """
    return get_db_manager().query_df(q)


def get_users(limit: int = 5000) -> pd.DataFrame:
    q = f"""
    SELECT
      user_id,
      student_email,
      name,
      role,
      department,
      cohort,
      date_added,
      date_updated
    FROM {_tbl('user')}
    ORDER BY date_added DESC
    LIMIT {limit}
    """
    return get_db_manager().query_df(q)


def get_sessions(user_id: Optional[str] = None, limit: int = 5000) -> pd.DataFrame:
    where = "" if not user_id else "WHERE user_id = @user_id"
    q = f"""
    SELECT
      session_id,
      case_study_id,
      user_id,
      user_email,
      start_time,
      end_time,
      is_active,
      last_activity,

      -- Derived fields (derived)
      TIMESTAMP_DIFF(end_time, start_time, SECOND) AS `session_duration_seconds [derived]`,
      TIMESTAMP_DIFF(end_time, start_time, MINUTE) AS `session_duration_minutes [derived]`
    FROM {_tbl('sessions')}
    {where}
    ORDER BY start_time DESC
    LIMIT {limit}
    """

    params = {"user_id": user_id} if user_id else None
    return get_db_manager().query_df(q, params=params)


def get_conversations(case_study_id: Optional[str] = None, user_id: Optional[str] = None, limit: int = 2000) -> pd.DataFrame:
    clauses = []
    params = {}
    if case_study_id:
        clauses.append("case_study_id = @case_study_id")
        params["case_study_id"] = case_study_id
    if user_id:
        clauses.append("user_id = @user_id")
        params["user_id"] = user_id
    where = "" if not clauses else "WHERE " + " AND ".join(clauses)

    q = f"""
    SELECT
      conversation_id,
      case_study_id,
      user_id,
      session_attempt,
      transcript,
      timestamp,

      -- Derived fields (derived)
      LENGTH(COALESCE(transcript, '')) AS `transcript_char_len [derived]`,
      ARRAY_LENGTH(SPLIT(REGEXP_REPLACE(COALESCE(transcript, ''), r'\\s+', ' '), ' ')) AS `transcript_word_count [derived]`
    FROM {_tbl('conversation')}
    {where}
    ORDER BY timestamp DESC
    LIMIT {limit}
    """

    return get_db_manager().query_df(q, params=params or None)


def get_grades(case_study_id: Optional[str] = None, user_id: Optional[str] = None, limit: int = 5000) -> pd.DataFrame:
    clauses = []
    params = {}
    if case_study_id:
        clauses.append("case_study_id = @case_study_id")
        params["case_study_id"] = case_study_id
    if user_id:
        clauses.append("user_id = @user_id")
        params["user_id"] = user_id
    where = "" if not clauses else "WHERE " + " AND ".join(clauses)

    q = f"""
    SELECT
      grade_id,
      user_id,
      case_study_id,
      conversation_id,
      attempt,
      timestamp,
      communication,
      comprehension,
      critical_thinking,
      performance_summary,
      overall_summary,
      final_score,

      -- Derived fields (derived)
      SAFE_DIVIDE(communication + comprehension + critical_thinking, 3) AS `rubric_avg_score [derived]`,
      CASE
        WHEN final_score >= 80 THEN 'excellent'
        WHEN final_score >= 60 THEN 'good'
        WHEN final_score >= 40 THEN 'needs_improvement'
        ELSE 'at_risk'
      END AS `performance_band [derived]`
    FROM {_tbl('grades')}
    {where}
    ORDER BY timestamp DESC
    LIMIT {limit}
    """

    return get_db_manager().query_df(q, params=params or None)


# -----------------------------
# Telemetry / analytics
# -----------------------------

def get_backend_telemetry(day: Optional[str] = None, limit: int = 10000) -> pd.DataFrame:
    where = "" if not day else "WHERE day = @day"
    q = f"""
    SELECT
      created_at,
      trace_id,
      span_id,
      kind,
      level,
      span_name,
      message,
      service_name,
      deployment_environment,
      http_method,
      url_path,
      http_response_status_code,
      SAFE_CAST(attributes_reduced AS STRING) AS attributes_reduced,
      day,

      -- Derived fields (derived)
      IFNULL(SAFE_CAST(http_response_status_code AS INT64), SAFE_CAST(`_lf_attributes/http.status_code` AS INT64)) AS `status_code [derived]`,
      IF(
        IFNULL(SAFE_CAST(http_response_status_code AS INT64), SAFE_CAST(`_lf_attributes/http.status_code` AS INT64)) >= 500,
        TRUE,
        FALSE
      ) AS `is_server_error [derived]`
    FROM {_tbl('backend_telemetry')}
    {where}
    ORDER BY created_at DESC
    LIMIT {limit}
    """
    params = {"day": day} if day else None
    return get_db_manager().query_df(q, params=params)


def get_web_sessions(limit: int = 10000) -> pd.DataFrame:
    q = f"""
    SELECT
      session_id,
      distinct_id,
      `$start_timestamp` AS start_timestamp,
      `$end_timestamp` AS end_timestamp,
      `$session_duration` AS session_duration,
      `$entry_current_url` AS entry_url,
      `$entry_pathname` AS entry_path,
      `$end_current_url` AS end_url,
      `$end_pathname` AS end_path,
      `$channel_type` AS channel_type,
      `$pageview_count` AS pageview_count,
      `$autocapture_count` AS autocapture_count,
      `$screen_count` AS screen_count,

      -- Derived fields (derived)
      SAFE_DIVIDE(`$pageview_count` + `$autocapture_count` + `$screen_count`, NULLIF(`$session_duration`, 0)) AS `events_per_second [derived]`
    FROM {_tbl('web_sessions')}
    ORDER BY start_timestamp DESC
    LIMIT {limit}
    """
    return get_db_manager().query_df(q)


def get_web_events(limit: int = 20000) -> pd.DataFrame:
    q = f"""
    SELECT
      uuid,
      event,
      timestamp,
      distinct_id,
      SAFE_CAST(properties AS STRING) AS properties_json,
      `$session_id` AS session_id,
      `$window_id` AS window_id,

      -- Derived fields (derived)
      STARTS_WITH(event, '$') AS `is_system_event [derived]`,
      IF(event = '$exception', TRUE, FALSE) AS `is_exception_event [derived]`
    FROM {_tbl('web_events')}
    ORDER BY timestamp DESC
    LIMIT {limit}
    """
    return get_db_manager().query_df(q)
