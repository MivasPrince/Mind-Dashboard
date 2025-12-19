"""
SQL queries for admin_aggregates and cross-cutting analytics
Provides functions for administrative dashboard
"""

from typing import Optional

def get_admin_aggregates(metric_names: Optional[list] = None) -> str:
    """
    Get administrative aggregate metrics
    
    Args:
        metric_names: Optional list of specific metrics to retrieve
        
    Returns:
        SQL query string
    """
    query = """
    SELECT 
        metric_id,
        metric_name,
        metric_value,
        timestamp,
        description
    FROM admin_aggregates
    """
    
    if metric_names:
        metrics_list = "','".join(metric_names)
        query += f" WHERE metric_name IN ('{metrics_list}')"
    
    query += " ORDER BY timestamp DESC, metric_name"
    
    return query

def get_platform_overview() -> str:
    """Get platform-wide overview statistics"""
    return """
    SELECT 
        (SELECT COUNT(DISTINCT student_id) FROM students WHERE role = 'Student') as total_students,
        (SELECT COUNT(DISTINCT student_id) FROM attempts WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days') as active_students_30d,
        (SELECT COUNT(*) FROM attempts) as total_attempts,
        (SELECT COUNT(*) FROM attempts WHERE state = 'Completed') as completed_attempts,
        (SELECT ROUND(AVG(score), 2) FROM attempts) as avg_score,
        (SELECT ROUND(AVG(ces_value), 2) FROM attempts WHERE ces_value IS NOT NULL) as avg_ces,
        (SELECT COUNT(DISTINCT cohort_id) FROM students WHERE cohort_id IS NOT NULL) as total_cohorts,
        (SELECT COUNT(DISTINCT campus) FROM students WHERE campus IS NOT NULL) as total_campuses,
        (SELECT COUNT(*) FROM case_studies) as total_cases
    """

def get_usage_by_campus() -> str:
    """Get usage statistics by campus"""
    return """
    SELECT 
        s.campus,
        COUNT(DISTINCT s.student_id) as student_count,
        COUNT(DISTINCT a.student_id) as active_students,
        COUNT(a.attempt_id) as total_attempts,
        AVG(a.score) as avg_score,
        AVG(a.ces_value) as avg_ces,
        AVG(a.duration_seconds) as avg_duration
    FROM students s
    LEFT JOIN attempts a ON s.student_id = a.student_id
    WHERE s.campus IS NOT NULL
    GROUP BY s.campus
    ORDER BY student_count DESC
    """

def get_usage_by_department() -> str:
    """Get usage statistics by department"""
    return """
    SELECT 
        s.department,
        COUNT(DISTINCT s.student_id) as student_count,
        COUNT(DISTINCT a.student_id) as active_students,
        COUNT(a.attempt_id) as total_attempts,
        AVG(a.score) as avg_score,
        AVG(a.ces_value) as avg_ces
    FROM students s
    LEFT JOIN attempts a ON s.student_id = a.student_id
    WHERE s.department IS NOT NULL
    GROUP BY s.department
    ORDER BY student_count DESC
    """

def get_case_study_performance_summary() -> str:
    """Get performance summary for all case studies"""
    return """
    SELECT 
        cs.case_id,
        cs.title,
        COUNT(DISTINCT a.student_id) as unique_students,
        COUNT(a.attempt_id) as total_attempts,
        AVG(a.score) as avg_score,
        AVG(a.duration_seconds) as avg_duration,
        AVG(a.ces_value) as avg_ces,
        SUM(CASE WHEN a.state = 'Completed' THEN 1 ELSE 0 END)::FLOAT / 
            NULLIF(COUNT(*), 0) * 100 as completion_rate
    FROM case_studies cs
    LEFT JOIN attempts a ON cs.case_id = a.case_id
    GROUP BY cs.case_id, cs.title
    ORDER BY total_attempts DESC
    """

def get_top_performing_cohorts(limit: int = 10) -> str:
    """Get top performing cohorts"""
    return f"""
    SELECT 
        s.cohort_id,
        COUNT(DISTINCT s.student_id) as student_count,
        COUNT(a.attempt_id) as total_attempts,
        AVG(a.score) as avg_score,
        AVG(a.ces_value) as avg_ces,
        AVG(a.duration_seconds) as avg_duration
    FROM students s
    INNER JOIN attempts a ON s.student_id = a.student_id
    WHERE s.cohort_id IS NOT NULL
    GROUP BY s.cohort_id
    HAVING COUNT(a.attempt_id) >= 10
    ORDER BY avg_score DESC
    LIMIT {limit}
    """

def get_bottom_performing_cohorts(limit: int = 10) -> str:
    """Get bottom performing cohorts"""
    return f"""
    SELECT 
        s.cohort_id,
        COUNT(DISTINCT s.student_id) as student_count,
        COUNT(a.attempt_id) as total_attempts,
        AVG(a.score) as avg_score,
        AVG(a.ces_value) as avg_ces,
        AVG(a.duration_seconds) as avg_duration
    FROM students s
    INNER JOIN attempts a ON s.student_id = a.student_id
    WHERE s.cohort_id IS NOT NULL
    GROUP BY s.cohort_id
    HAVING COUNT(a.attempt_id) >= 10
    ORDER BY avg_score ASC
    LIMIT {limit}
    """

def get_daily_active_users_trend(days: int = 30) -> str:
    """Get daily active users trend"""
    return f"""
    SELECT 
        DATE(timestamp) as date,
        COUNT(DISTINCT student_id) as active_users,
        COUNT(*) as total_attempts,
        AVG(score) as avg_score
    FROM attempts
    WHERE timestamp >= CURRENT_DATE - INTERVAL '{days} days'
    GROUP BY date
    ORDER BY date ASC
    """

def get_weekly_metrics_trend(weeks: int = 12) -> str:
    """Get weekly aggregated metrics"""
    return f"""
    SELECT 
        DATE_TRUNC('week', timestamp) as week,
        COUNT(DISTINCT student_id) as active_students,
        COUNT(*) as total_attempts,
        AVG(score) as avg_score,
        AVG(ces_value) as avg_ces,
        AVG(duration_seconds) as avg_duration
    FROM attempts
    WHERE timestamp >= CURRENT_DATE - INTERVAL '{weeks} weeks'
    GROUP BY week
    ORDER BY week ASC
    """

def get_overall_system_health() -> str:
    """Get overall system health metrics"""
    return """
    WITH recent_reliability AS (
        SELECT 
            AVG(reliability_index) as avg_reliability,
            AVG(latency_ms) as avg_latency,
            AVG(error_rate) as avg_error_rate
        FROM system_reliability
        WHERE timestamp >= NOW() - INTERVAL '24 hours'
    ),
    recent_environment AS (
        SELECT 
            AVG(internet_stability_score) as avg_stability,
            AVG(internet_latency_ms) as avg_env_latency,
            AVG(noise_quality_index) as avg_noise_quality
        FROM environment_metrics em
        INNER JOIN attempts a ON em.attempt_id = a.attempt_id
        WHERE a.timestamp >= CURRENT_DATE - INTERVAL '7 days'
    )
    SELECT 
        rr.avg_reliability,
        rr.avg_latency,
        rr.avg_error_rate,
        re.avg_stability,
        re.avg_env_latency,
        re.avg_noise_quality
    FROM recent_reliability rr
    CROSS JOIN recent_environment re
    """

def get_key_incidents_summary(days: int = 7) -> str:
    """Get summary of key incidents"""
    return f"""
    SELECT 
        severity,
        location,
        COUNT(*) as incident_count,
        AVG(latency_ms) as avg_latency,
        AVG(error_rate) as avg_error_rate,
        MAX(timestamp) as last_occurrence
    FROM system_reliability
    WHERE timestamp >= CURRENT_DATE - INTERVAL '{days} days'
    AND severity IN ('Warning', 'Critical')
    GROUP BY severity, location
    ORDER BY severity DESC, incident_count DESC
    """

def get_engagement_summary() -> str:
    """Get platform-wide engagement summary"""
    return """
    SELECT 
        COUNT(DISTINCT student_id) as engaged_students,
        COUNT(DISTINCT session_id) as total_sessions,
        COUNT(*) as total_actions,
        SUM(duration_seconds) as total_duration_seconds,
        AVG(duration_seconds) as avg_action_duration,
        COUNT(DISTINCT DATE(timestamp)) as active_days
    FROM engagement_logs
    WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
    """

def get_improvement_metrics() -> str:
    """Get platform-wide improvement metrics"""
    return """
    WITH attempt_improvements AS (
        SELECT 
            a1.student_id,
            a1.case_id,
            a1.score as attempt1_score,
            a2.score as attempt2_score,
            a2.score - a1.score as improvement
        FROM attempts a1
        INNER JOIN attempts a2 
            ON a1.student_id = a2.student_id 
            AND a1.case_id = a2.case_id
            AND a1.attempt_number = 1 
            AND a2.attempt_number = 2
    )
    SELECT 
        COUNT(*) as total_with_second_attempt,
        AVG(improvement) as avg_improvement,
        SUM(CASE WHEN improvement > 0 THEN 1 ELSE 0 END)::FLOAT / 
            COUNT(*) * 100 as pct_improved,
        MAX(improvement) as max_improvement,
        MIN(improvement) as min_improvement
    FROM attempt_improvements
    """

def get_role_distribution() -> str:
    """Get distribution of users by role"""
    return """
    SELECT 
        role,
        COUNT(*) as user_count
    FROM students
    GROUP BY role
    ORDER BY user_count DESC
    """
