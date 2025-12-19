"""
SQL queries for engagement_logs table
Provides functions to query student engagement data
"""

from typing import Optional

def get_student_engagement(student_id: str, start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> str:
    """
    Get engagement logs for a student
    
    Args:
        student_id: Student ID
        start_date: Optional start date filter
        end_date: Optional end date filter
        
    Returns:
        SQL query string
    """
    query = f"""
    SELECT 
        el.session_id,
        el.case_id,
        cs.title as case_title,
        el.attempt_id,
        el.timestamp,
        el.action_type,
        el.duration_seconds,
        el.session_phase
    FROM engagement_logs el
    LEFT JOIN case_studies cs ON el.case_id = cs.case_id
    WHERE el.student_id = '{student_id}'
    """
    
    if start_date:
        query += f" AND el.timestamp >= '{start_date}'"
    if end_date:
        query += f" AND el.timestamp <= '{end_date}'"
    
    query += " ORDER BY el.timestamp DESC"
    
    return query

def get_student_active_days(student_id: str) -> str:
    """
    Count active days for a student
    
    Args:
        student_id: Student ID
        
    Returns:
        SQL query string
    """
    return f"""
    SELECT 
        COUNT(DISTINCT DATE(timestamp)) as active_days
    FROM engagement_logs
    WHERE student_id = '{student_id}'
    """

def get_engagement_summary_by_student(student_id: str) -> str:
    """
    Get engagement summary metrics for a student
    
    Args:
        student_id: Student ID
        
    Returns:
        SQL query string
    """
    return f"""
    SELECT 
        COUNT(DISTINCT session_id) as total_sessions,
        COUNT(DISTINCT case_id) as cases_engaged,
        COUNT(*) as total_actions,
        SUM(duration_seconds) as total_duration_seconds,
        AVG(duration_seconds) as avg_action_duration,
        COUNT(DISTINCT action_type) as unique_action_types
    FROM engagement_logs
    WHERE student_id = '{student_id}'
    """

def get_daily_engagement_trend(student_id: str, days: int = 30) -> str:
    """
    Get daily engagement trend for a student
    
    Args:
        student_id: Student ID
        days: Number of days to look back
        
    Returns:
        SQL query string
    """
    return f"""
    SELECT 
        DATE(timestamp) as date,
        COUNT(*) as action_count,
        SUM(duration_seconds) as total_duration,
        COUNT(DISTINCT session_id) as session_count,
        COUNT(DISTINCT case_id) as case_count
    FROM engagement_logs
    WHERE student_id = '{student_id}'
    AND timestamp >= CURRENT_DATE - INTERVAL '{days} days'
    GROUP BY DATE(timestamp)
    ORDER BY date ASC
    """

def get_engagement_by_action_type(student_id: str) -> str:
    """
    Get engagement breakdown by action type
    
    Args:
        student_id: Student ID
        
    Returns:
        SQL query string
    """
    return f"""
    SELECT 
        action_type,
        COUNT(*) as action_count,
        SUM(duration_seconds) as total_duration,
        AVG(duration_seconds) as avg_duration
    FROM engagement_logs
    WHERE student_id = '{student_id}'
    GROUP BY action_type
    ORDER BY action_count DESC
    """

def get_engagement_by_session_phase(student_id: str) -> str:
    """
    Get engagement breakdown by session phase
    
    Args:
        student_id: Student ID
        
    Returns:
        SQL query string
    """
    return f"""
    SELECT 
        session_phase,
        COUNT(*) as action_count,
        SUM(duration_seconds) as total_duration,
        AVG(duration_seconds) as avg_duration,
        COUNT(DISTINCT session_id) as session_count
    FROM engagement_logs
    WHERE student_id = '{student_id}'
    AND session_phase IS NOT NULL
    GROUP BY session_phase
    ORDER BY total_duration DESC
    """

def get_cohort_engagement_summary(cohort_id: str, start_date: Optional[str] = None,
                                 end_date: Optional[str] = None) -> str:
    """
    Get engagement summary for a cohort
    
    Args:
        cohort_id: Cohort ID
        start_date: Optional start date filter
        end_date: Optional end date filter
        
    Returns:
        SQL query string
    """
    query = f"""
    SELECT 
        el.student_id,
        s.name as student_name,
        COUNT(DISTINCT el.session_id) as total_sessions,
        COUNT(*) as total_actions,
        SUM(el.duration_seconds) as total_duration_seconds,
        AVG(el.duration_seconds) as avg_action_duration,
        COUNT(DISTINCT DATE(el.timestamp)) as active_days
    FROM engagement_logs el
    INNER JOIN students s ON el.student_id = s.student_id
    WHERE s.cohort_id = '{cohort_id}'
    """
    
    if start_date:
        query += f" AND el.timestamp >= '{start_date}'"
    if end_date:
        query += f" AND el.timestamp <= '{end_date}'"
    
    query += """
    GROUP BY el.student_id, s.name
    ORDER BY total_duration_seconds DESC
    """
    
    return query

def get_case_engagement_metrics(case_id: str) -> str:
    """
    Get engagement metrics for a specific case
    
    Args:
        case_id: Case ID
        
    Returns:
        SQL query string
    """
    return f"""
    SELECT 
        COUNT(DISTINCT student_id) as unique_students,
        COUNT(DISTINCT session_id) as total_sessions,
        COUNT(*) as total_actions,
        SUM(duration_seconds) as total_duration,
        AVG(duration_seconds) as avg_action_duration,
        COUNT(DISTINCT action_type) as unique_actions
    FROM engagement_logs
    WHERE case_id = '{case_id}'
    """

def get_low_engagement_students(cohort_id: str, min_hours: float = 1.0) -> str:
    """
    Identify students with low engagement
    
    Args:
        cohort_id: Cohort ID
        min_hours: Minimum engagement hours threshold
        
    Returns:
        SQL query string
    """
    min_seconds = min_hours * 3600
    
    return f"""
    SELECT 
        s.student_id,
        s.name as student_name,
        COALESCE(SUM(el.duration_seconds), 0) as total_duration_seconds,
        COALESCE(COUNT(DISTINCT el.session_id), 0) as session_count,
        COALESCE(MAX(el.timestamp), NULL) as last_activity
    FROM students s
    LEFT JOIN engagement_logs el ON s.student_id = el.student_id
    WHERE s.cohort_id = '{cohort_id}'
    GROUP BY s.student_id, s.name
    HAVING COALESCE(SUM(el.duration_seconds), 0) < {min_seconds}
    ORDER BY total_duration_seconds ASC
    """

def get_peak_engagement_hours() -> str:
    """
    Get peak engagement hours across all students
    
    Returns:
        SQL query string
    """
    return """
    SELECT 
        EXTRACT(HOUR FROM timestamp) as hour_of_day,
        COUNT(*) as action_count,
        COUNT(DISTINCT student_id) as unique_students,
        SUM(duration_seconds) as total_duration
    FROM engagement_logs
    GROUP BY hour_of_day
    ORDER BY hour_of_day
    """
