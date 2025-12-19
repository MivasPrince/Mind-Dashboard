"""
SQL queries for attempts table
Provides functions to query student attempt data
"""

from typing import Optional, List
import pandas as pd

def get_student_attempts(student_id: str, start_date: Optional[str] = None, 
                        end_date: Optional[str] = None) -> str:
    """
    Get all attempts for a specific student
    
    Args:
        student_id: Student ID
        start_date: Optional start date filter (ISO format)
        end_date: Optional end date filter (ISO format)
        
    Returns:
        SQL query string
    """
    query = f"""
    SELECT 
        a.attempt_id,
        a.student_id,
        a.case_id,
        cs.title as case_title,
        a.attempt_number,
        a.score,
        a.duration_seconds,
        a.ces_value,
        a.timestamp,
        a.state
    FROM attempts a
    LEFT JOIN case_studies cs ON a.case_id = cs.case_id
    WHERE a.student_id = '{student_id}'
    """
    
    if start_date:
        query += f" AND a.timestamp >= '{start_date}'"
    if end_date:
        query += f" AND a.timestamp <= '{end_date}'"
    
    query += " ORDER BY a.timestamp DESC"
    
    return query

def get_student_performance_summary(student_id: str) -> str:
    """
    Get performance summary for a student
    
    Args:
        student_id: Student ID
        
    Returns:
        SQL query string
    """
    return f"""
    WITH latest_attempts AS (
        SELECT 
            case_id,
            MAX(attempt_number) as max_attempt,
            MAX(timestamp) as latest_timestamp
        FROM attempts
        WHERE student_id = '{student_id}'
        GROUP BY case_id
    ),
    attempt_scores AS (
        SELECT 
            a.case_id,
            cs.title as case_title,
            a.attempt_number,
            a.score,
            a.duration_seconds,
            a.ces_value
        FROM attempts a
        INNER JOIN latest_attempts la 
            ON a.case_id = la.case_id 
            AND a.attempt_number = la.max_attempt
            AND a.timestamp = la.latest_timestamp
        LEFT JOIN case_studies cs ON a.case_id = cs.case_id
        WHERE a.student_id = '{student_id}'
    )
    SELECT 
        COUNT(DISTINCT case_id) as total_cases_attempted,
        AVG(score) as avg_score,
        AVG(duration_seconds) as avg_duration,
        AVG(ces_value) as avg_ces,
        MIN(score) as min_score,
        MAX(score) as max_score
    FROM attempt_scores
    """

def get_attempt_improvement(student_id: str) -> str:
    """
    Calculate improvement between attempt 1 and 2 for each case
    
    Args:
        student_id: Student ID
        
    Returns:
        SQL query string
    """
    return f"""
    WITH attempt_data AS (
        SELECT 
            a.case_id,
            cs.title as case_title,
            a.attempt_number,
            a.score
        FROM attempts a
        LEFT JOIN case_studies cs ON a.case_id = cs.case_id
        WHERE a.student_id = '{student_id}'
        AND a.attempt_number IN (1, 2)
    ),
    pivoted AS (
        SELECT 
            case_id,
            case_title,
            MAX(CASE WHEN attempt_number = 1 THEN score END) as attempt1_score,
            MAX(CASE WHEN attempt_number = 2 THEN score END) as attempt2_score
        FROM attempt_data
        GROUP BY case_id, case_title
    )
    SELECT 
        case_id,
        case_title,
        attempt1_score,
        attempt2_score,
        CASE 
            WHEN attempt2_score IS NOT NULL AND attempt1_score IS NOT NULL 
            THEN attempt2_score - attempt1_score 
            ELSE NULL 
        END as improvement
    FROM pivoted
    WHERE attempt1_score IS NOT NULL
    ORDER BY improvement DESC NULLS LAST
    """

def get_score_trend(student_id: str) -> str:
    """
    Get score trend over time for a student
    
    Args:
        student_id: Student ID
        
    Returns:
        SQL query string
    """
    return f"""
    WITH ranked_attempts AS (
        SELECT 
            a.attempt_id,
            a.case_id,
            cs.title as case_title,
            a.score,
            a.timestamp,
            ROW_NUMBER() OVER (PARTITION BY a.case_id ORDER BY a.timestamp DESC) as rn
        FROM attempts a
        LEFT JOIN case_studies cs ON a.case_id = cs.case_id
        WHERE a.student_id = '{student_id}'
    )
    SELECT 
        attempt_id,
        case_id,
        case_title,
        score,
        timestamp
    FROM ranked_attempts
    WHERE rn = 1
    ORDER BY timestamp ASC
    """

def get_attempts_by_case(case_id: str, start_date: Optional[str] = None,
                        end_date: Optional[str] = None) -> str:
    """
    Get all attempts for a specific case
    
    Args:
        case_id: Case study ID
        start_date: Optional start date filter
        end_date: Optional end date filter
        
    Returns:
        SQL query string
    """
    query = f"""
    SELECT 
        a.attempt_id,
        a.student_id,
        s.name as student_name,
        s.cohort_id,
        a.attempt_number,
        a.score,
        a.duration_seconds,
        a.ces_value,
        a.timestamp,
        a.state
    FROM attempts a
    LEFT JOIN students s ON a.student_id = s.student_id
    WHERE a.case_id = '{case_id}'
    """
    
    if start_date:
        query += f" AND a.timestamp >= '{start_date}'"
    if end_date:
        query += f" AND a.timestamp <= '{end_date}'"
    
    query += " ORDER BY a.timestamp DESC"
    
    return query

def get_cohort_performance(cohort_id: str, start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> str:
    """
    Get performance metrics for a cohort
    
    Args:
        cohort_id: Cohort ID
        start_date: Optional start date filter
        end_date: Optional end date filter
        
    Returns:
        SQL query string
    """
    query = f"""
    SELECT 
        a.student_id,
        s.name as student_name,
        COUNT(DISTINCT a.case_id) as cases_attempted,
        AVG(a.score) as avg_score,
        AVG(a.duration_seconds) as avg_duration,
        AVG(a.ces_value) as avg_ces,
        MAX(a.timestamp) as last_attempt_date
    FROM attempts a
    INNER JOIN students s ON a.student_id = s.student_id
    WHERE s.cohort_id = '{cohort_id}'
    """
    
    if start_date:
        query += f" AND a.timestamp >= '{start_date}'"
    if end_date:
        query += f" AND a.timestamp <= '{end_date}'"
    
    query += """
    GROUP BY a.student_id, s.name
    ORDER BY avg_score DESC
    """
    
    return query

def get_attempt_statistics_by_case() -> str:
    """
    Get aggregated statistics for each case study
    
    Returns:
        SQL query string
    """
    return """
    WITH attempt_stats AS (
        SELECT 
            a.case_id,
            cs.title as case_title,
            a.attempt_number,
            COUNT(*) as attempt_count,
            AVG(a.score) as avg_score,
            AVG(a.duration_seconds) as avg_duration,
            AVG(a.ces_value) as avg_ces
        FROM attempts a
        LEFT JOIN case_studies cs ON a.case_id = cs.case_id
        GROUP BY a.case_id, cs.title, a.attempt_number
    )
    SELECT 
        case_id,
        case_title,
        SUM(attempt_count) as total_attempts,
        MAX(CASE WHEN attempt_number = 1 THEN avg_score END) as avg_attempt1_score,
        MAX(CASE WHEN attempt_number = 2 THEN avg_score END) as avg_attempt2_score,
        MAX(CASE WHEN attempt_number = 1 THEN avg_duration END) as avg_attempt1_duration,
        MAX(CASE WHEN attempt_number = 2 THEN avg_duration END) as avg_attempt2_duration,
        AVG(avg_ces) as avg_ces
    FROM attempt_stats
    GROUP BY case_id, case_title
    ORDER BY total_attempts DESC
    """

def get_active_students(start_date: str, end_date: str) -> str:
    """
    Get count of active students in date range
    
    Args:
        start_date: Start date (ISO format)
        end_date: End date (ISO format)
        
    Returns:
        SQL query string
    """
    return f"""
    SELECT 
        COUNT(DISTINCT student_id) as active_students
    FROM attempts
    WHERE timestamp >= '{start_date}'
    AND timestamp <= '{end_date}'
    """

def get_completion_rate_by_case() -> str:
    """
    Get completion rate for each case study
    
    Returns:
        SQL query string
    """
    return """
    SELECT 
        a.case_id,
        cs.title as case_title,
        COUNT(*) as total_attempts,
        SUM(CASE WHEN a.state = 'Completed' THEN 1 ELSE 0 END) as completed_attempts,
        ROUND(
            SUM(CASE WHEN a.state = 'Completed' THEN 1 ELSE 0 END)::NUMERIC / 
            COUNT(*)::NUMERIC * 100, 
            2
        ) as completion_rate
    FROM attempts a
    LEFT JOIN case_studies cs ON a.case_id = cs.case_id
    GROUP BY a.case_id, cs.title
    ORDER BY completion_rate DESC
    """
