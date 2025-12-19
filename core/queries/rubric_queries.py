"""
SQL queries for rubric_scores table
Provides functions to query rubric scoring data
"""

from typing import Optional

def get_student_rubric_scores(student_id: str, case_id: Optional[str] = None) -> str:
    """
    Get rubric scores for a student
    
    Args:
        student_id: Student ID
        case_id: Optional case ID filter
        
    Returns:
        SQL query string
    """
    query = f"""
    SELECT 
        rs.rubric_score_id,
        rs.attempt_id,
        a.case_id,
        cs.title as case_title,
        a.attempt_number,
        rs.rubric_dimension,
        rs.score,
        rs.max_score,
        ROUND((rs.score::NUMERIC / rs.max_score::NUMERIC) * 100, 2) as percentage,
        rs.comment,
        rs.improvement_flag
    FROM rubric_scores rs
    INNER JOIN attempts a ON rs.attempt_id = a.attempt_id
    LEFT JOIN case_studies cs ON a.case_id = cs.case_id
    WHERE a.student_id = '{student_id}'
    """
    
    if case_id:
        query += f" AND a.case_id = '{case_id}'"
    
    query += " ORDER BY a.timestamp DESC, rs.rubric_dimension"
    
    return query

def get_rubric_mastery_by_dimension(student_id: str) -> str:
    """
    Get average rubric mastery by dimension for a student
    
    Args:
        student_id: Student ID
        
    Returns:
        SQL query string
    """
    return f"""
    SELECT 
        rs.rubric_dimension,
        COUNT(*) as total_scores,
        AVG(rs.score) as avg_score,
        AVG(rs.max_score) as avg_max_score,
        ROUND(AVG(rs.score::NUMERIC / rs.max_score::NUMERIC) * 100, 2) as avg_percentage,
        SUM(CASE WHEN rs.improvement_flag = TRUE THEN 1 ELSE 0 END) as improvements_count
    FROM rubric_scores rs
    INNER JOIN attempts a ON rs.attempt_id = a.attempt_id
    WHERE a.student_id = '{student_id}'
    GROUP BY rs.rubric_dimension
    ORDER BY avg_percentage DESC
    """

def get_cohort_rubric_performance(cohort_id: str) -> str:
    """
    Get rubric performance for a cohort
    
    Args:
        cohort_id: Cohort ID
        
    Returns:
        SQL query string
    """
    return f"""
    SELECT 
        rs.rubric_dimension,
        COUNT(DISTINCT a.student_id) as student_count,
        COUNT(*) as total_assessments,
        AVG(rs.score) as avg_score,
        AVG(rs.max_score) as avg_max_score,
        ROUND(AVG(rs.score::NUMERIC / rs.max_score::NUMERIC) * 100, 2) as avg_percentage,
        MIN(rs.score::NUMERIC / rs.max_score::NUMERIC * 100) as min_percentage,
        MAX(rs.score::NUMERIC / rs.max_score::NUMERIC * 100) as max_percentage
    FROM rubric_scores rs
    INNER JOIN attempts a ON rs.attempt_id = a.attempt_id
    INNER JOIN students s ON a.student_id = s.student_id
    WHERE s.cohort_id = '{cohort_id}'
    GROUP BY rs.rubric_dimension
    ORDER BY avg_percentage DESC
    """

def get_rubric_heatmap_data(case_ids: Optional[list] = None) -> str:
    """
    Get rubric dimension performance across cases for heatmap visualization
    
    Args:
        case_ids: Optional list of case IDs to filter
        
    Returns:
        SQL query string
    """
    query = """
    SELECT 
        a.case_id,
        cs.title as case_title,
        rs.rubric_dimension,
        ROUND(AVG(rs.score::NUMERIC / rs.max_score::NUMERIC) * 100, 2) as avg_percentage
    FROM rubric_scores rs
    INNER JOIN attempts a ON rs.attempt_id = a.attempt_id
    LEFT JOIN case_studies cs ON a.case_id = cs.case_id
    """
    
    if case_ids:
        case_list = "','".join(case_ids)
        query += f" WHERE a.case_id IN ('{case_list}')"
    
    query += """
    GROUP BY a.case_id, cs.title, rs.rubric_dimension
    ORDER BY a.case_id, rs.rubric_dimension
    """
    
    return query

def get_improvement_flagged_scores(student_id: Optional[str] = None) -> str:
    """
    Get scores flagged for improvement
    
    Args:
        student_id: Optional student ID filter
        
    Returns:
        SQL query string
    """
    query = """
    SELECT 
        a.student_id,
        s.name as student_name,
        a.case_id,
        cs.title as case_title,
        a.attempt_number,
        rs.rubric_dimension,
        rs.score,
        rs.max_score,
        ROUND((rs.score::NUMERIC / rs.max_score::NUMERIC) * 100, 2) as percentage,
        rs.comment,
        a.timestamp
    FROM rubric_scores rs
    INNER JOIN attempts a ON rs.attempt_id = a.attempt_id
    LEFT JOIN students s ON a.student_id = s.student_id
    LEFT JOIN case_studies cs ON a.case_id = cs.case_id
    WHERE rs.improvement_flag = TRUE
    """
    
    if student_id:
        query += f" AND a.student_id = '{student_id}'"
    
    query += " ORDER BY a.timestamp DESC"
    
    return query

def get_rubric_dimension_distribution(dimension: str) -> str:
    """
    Get score distribution for a specific rubric dimension
    
    Args:
        dimension: Rubric dimension name
        
    Returns:
        SQL query string
    """
    return f"""
    SELECT 
        ROUND((rs.score::NUMERIC / rs.max_score::NUMERIC) * 100, 2) as percentage,
        COUNT(*) as frequency
    FROM rubric_scores rs
    WHERE rs.rubric_dimension = '{dimension}'
    GROUP BY percentage
    ORDER BY percentage
    """

def get_student_rubric_detail(student_id: str, case_id: str) -> str:
    """
    Get detailed rubric breakdown for a student's case
    
    Args:
        student_id: Student ID
        case_id: Case ID
        
    Returns:
        SQL query string
    """
    return f"""
    WITH latest_attempt AS (
        SELECT MAX(attempt_number) as max_attempt
        FROM attempts
        WHERE student_id = '{student_id}' AND case_id = '{case_id}'
    )
    SELECT 
        rs.rubric_dimension,
        rs.score,
        rs.max_score,
        ROUND((rs.score::NUMERIC / rs.max_score::NUMERIC) * 100, 2) as percentage,
        rs.comment,
        rs.improvement_flag,
        a.attempt_number,
        a.timestamp
    FROM rubric_scores rs
    INNER JOIN attempts a ON rs.attempt_id = a.attempt_id
    INNER JOIN latest_attempt la ON a.attempt_number = la.max_attempt
    WHERE a.student_id = '{student_id}' AND a.case_id = '{case_id}'
    ORDER BY rs.rubric_dimension
    """

def get_top_performers_by_dimension(dimension: str, limit: int = 10) -> str:
    """
    Get top performing students in a specific rubric dimension
    
    Args:
        dimension: Rubric dimension name
        limit: Number of top performers to return
        
    Returns:
        SQL query string
    """
    return f"""
    SELECT 
        a.student_id,
        s.name as student_name,
        s.cohort_id,
        COUNT(*) as assessments_count,
        ROUND(AVG(rs.score::NUMERIC / rs.max_score::NUMERIC) * 100, 2) as avg_percentage
    FROM rubric_scores rs
    INNER JOIN attempts a ON rs.attempt_id = a.attempt_id
    LEFT JOIN students s ON a.student_id = s.student_id
    WHERE rs.rubric_dimension = '{dimension}'
    GROUP BY a.student_id, s.name, s.cohort_id
    HAVING COUNT(*) >= 3
    ORDER BY avg_percentage DESC
    LIMIT {limit}
    """

def get_rubric_comments_for_review(case_id: Optional[str] = None) -> str:
    """
    Get all rubric comments for review
    
    Args:
        case_id: Optional case ID filter
        
    Returns:
        SQL query string
    """
    query = """
    SELECT 
        rs.rubric_score_id,
        a.student_id,
        s.name as student_name,
        a.case_id,
        cs.title as case_title,
        rs.rubric_dimension,
        rs.score,
        rs.max_score,
        rs.comment,
        rs.improvement_flag,
        a.timestamp
    FROM rubric_scores rs
    INNER JOIN attempts a ON rs.attempt_id = a.attempt_id
    LEFT JOIN students s ON a.student_id = s.student_id
    LEFT JOIN case_studies cs ON a.case_id = cs.case_id
    WHERE rs.comment IS NOT NULL AND rs.comment != ''
    """
    
    if case_id:
        query += f" AND a.case_id = '{case_id}'"
    
    query += " ORDER BY a.timestamp DESC"
    
    return query
