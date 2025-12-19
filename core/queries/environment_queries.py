"""
SQL queries for environment_metrics and system_reliability tables
Provides functions for developer dashboard
"""

from typing import Optional, List

# ============================================
# ENVIRONMENT METRICS QUERIES
# ============================================

def get_environment_metrics_for_attempt(attempt_id: str) -> str:
    """Get environment metrics for a specific attempt"""
    return f"""
    SELECT 
        em.*,
        a.score,
        a.timestamp,
        cs.title as case_title
    FROM environment_metrics em
    LEFT JOIN attempts a ON em.attempt_id = a.attempt_id
    LEFT JOIN case_studies cs ON em.case_id = cs.case_id
    WHERE em.attempt_id = '{attempt_id}'
    """

def get_student_environment_history(student_id: str) -> str:
    """Get environment quality history for a student"""
    return f"""
    SELECT 
        em.attempt_id,
        em.case_id,
        cs.title as case_title,
        em.noise_level,
        em.noise_quality_index,
        em.internet_latency_ms,
        em.internet_stability_score,
        em.connection_drops,
        em.device_type,
        em.microphone_type,
        em.signal_strength,
        a.score,
        a.timestamp
    FROM environment_metrics em
    INNER JOIN attempts a ON em.attempt_id = a.attempt_id
    LEFT JOIN case_studies cs ON em.case_id = cs.case_id
    WHERE em.student_id = '{student_id}'
    ORDER BY a.timestamp DESC
    """

def get_environment_quality_distribution() -> str:
    """Get distribution of environment quality metrics"""
    return """
    SELECT 
        CASE 
            WHEN noise_level <= 40 THEN 'Low (0-40 dB)'
            WHEN noise_level <= 60 THEN 'Moderate (41-60 dB)'
            WHEN noise_level <= 80 THEN 'High (61-80 dB)'
            ELSE 'Very High (>80 dB)'
        END as noise_category,
        CASE 
            WHEN internet_stability_score >= 80 THEN 'Excellent (80-100)'
            WHEN internet_stability_score >= 60 THEN 'Good (60-79)'
            WHEN internet_stability_score >= 40 THEN 'Fair (40-59)'
            ELSE 'Poor (<40)'
        END as stability_category,
        COUNT(*) as attempt_count,
        AVG(internet_latency_ms) as avg_latency,
        AVG(connection_drops) as avg_drops
    FROM environment_metrics
    GROUP BY noise_category, stability_category
    ORDER BY noise_category, stability_category
    """

def get_environment_impact_on_performance() -> str:
    """Analyze correlation between environment and performance"""
    return """
    SELECT 
        CASE 
            WHEN em.internet_latency_ms <= 50 THEN 'Low Latency (≤50ms)'
            WHEN em.internet_latency_ms <= 100 THEN 'Medium Latency (51-100ms)'
            WHEN em.internet_latency_ms <= 200 THEN 'High Latency (101-200ms)'
            ELSE 'Very High Latency (>200ms)'
        END as latency_category,
        COUNT(*) as attempt_count,
        AVG(a.score) as avg_score,
        AVG(a.duration_seconds) as avg_duration,
        AVG(em.connection_drops) as avg_connection_drops
    FROM environment_metrics em
    INNER JOIN attempts a ON em.attempt_id = a.attempt_id
    WHERE em.internet_latency_ms IS NOT NULL
    GROUP BY latency_category
    ORDER BY 
        CASE 
            WHEN latency_category = 'Low Latency (≤50ms)' THEN 1
            WHEN latency_category = 'Medium Latency (51-100ms)' THEN 2
            WHEN latency_category = 'High Latency (101-200ms)' THEN 3
            ELSE 4
        END
    """

def get_device_type_distribution() -> str:
    """Get distribution of device types"""
    return """
    SELECT 
        device_type,
        microphone_type,
        COUNT(*) as usage_count,
        AVG(noise_quality_index) as avg_noise_quality,
        AVG(internet_stability_score) as avg_stability
    FROM environment_metrics
    WHERE device_type IS NOT NULL
    GROUP BY device_type, microphone_type
    ORDER BY usage_count DESC
    """

def get_poor_environment_attempts(threshold: int = 50) -> str:
    """Get attempts with poor environment quality"""
    return f"""
    SELECT 
        em.attempt_id,
        em.student_id,
        s.name as student_name,
        em.case_id,
        cs.title as case_title,
        em.noise_level,
        em.noise_quality_index,
        em.internet_latency_ms,
        em.internet_stability_score,
        em.connection_drops,
        a.score,
        a.timestamp
    FROM environment_metrics em
    INNER JOIN attempts a ON em.attempt_id = a.attempt_id
    LEFT JOIN students s ON em.student_id = s.student_id
    LEFT JOIN case_studies cs ON em.case_id = cs.case_id
    WHERE em.internet_stability_score < {threshold}
       OR em.noise_level > 80
       OR em.internet_latency_ms > 200
    ORDER BY a.timestamp DESC
    LIMIT 100
    """

# ============================================
# SYSTEM RELIABILITY QUERIES
# ============================================

def get_system_reliability_overview(hours: int = 24) -> str:
    """Get system reliability overview for last N hours"""
    return f"""
    SELECT 
        api_name,
        COUNT(*) as total_records,
        AVG(latency_ms) as avg_latency,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY latency_ms) as p50_latency,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms) as p95_latency,
        AVG(error_rate) as avg_error_rate,
        AVG(reliability_index) as avg_reliability,
        SUM(CASE WHEN severity = 'Critical' THEN 1 ELSE 0 END) as critical_count,
        SUM(CASE WHEN severity = 'Warning' THEN 1 ELSE 0 END) as warning_count
    FROM system_reliability
    WHERE timestamp >= NOW() - INTERVAL '{hours} hours'
    GROUP BY api_name
    ORDER BY avg_reliability DESC
    """

def get_latency_trend(api_name: str, hours: int = 24) -> str:
    """Get latency trend for specific API"""
    return f"""
    SELECT 
        DATE_TRUNC('hour', timestamp) as hour,
        AVG(latency_ms) as avg_latency,
        MIN(latency_ms) as min_latency,
        MAX(latency_ms) as max_latency,
        COUNT(*) as record_count
    FROM system_reliability
    WHERE api_name = '{api_name}'
    AND timestamp >= NOW() - INTERVAL '{hours} hours'
    GROUP BY hour
    ORDER BY hour ASC
    """

def get_error_rate_by_api(hours: int = 24) -> str:
    """Get error rates by API"""
    return f"""
    SELECT 
        api_name,
        AVG(error_rate) as avg_error_rate,
        MAX(error_rate) as max_error_rate,
        COUNT(*) as sample_count
    FROM system_reliability
    WHERE timestamp >= NOW() - INTERVAL '{hours} hours'
    GROUP BY api_name
    ORDER BY avg_error_rate DESC
    """

def get_critical_incidents(days: int = 7) -> str:
    """Get critical incidents"""
    return f"""
    SELECT 
        record_id,
        api_name,
        latency_ms,
        error_rate,
        reliability_index,
        timestamp,
        location,
        severity
    FROM system_reliability
    WHERE severity = 'Critical'
    AND timestamp >= NOW() - INTERVAL '{days} days'
    ORDER BY timestamp DESC
    LIMIT 100
    """

def get_reliability_by_location(hours: int = 24) -> str:
    """Get reliability metrics by location"""
    return f"""
    SELECT 
        location,
        COUNT(*) as total_records,
        AVG(latency_ms) as avg_latency,
        AVG(error_rate) as avg_error_rate,
        AVG(reliability_index) as avg_reliability,
        SUM(CASE WHEN severity = 'Critical' THEN 1 ELSE 0 END) as critical_count
    FROM system_reliability
    WHERE timestamp >= NOW() - INTERVAL '{hours} hours'
    AND location IS NOT NULL
    GROUP BY location
    ORDER BY avg_reliability DESC
    """

def get_reliability_trend_over_time(days: int = 7) -> str:
    """Get overall reliability trend"""
    return f"""
    SELECT 
        DATE(timestamp) as date,
        AVG(reliability_index) as avg_reliability,
        AVG(latency_ms) as avg_latency,
        AVG(error_rate) as avg_error_rate,
        SUM(CASE WHEN severity = 'Critical' THEN 1 ELSE 0 END) as critical_incidents
    FROM system_reliability
    WHERE timestamp >= CURRENT_DATE - INTERVAL '{days} days'
    GROUP BY date
    ORDER BY date ASC
    """

def get_api_performance_summary() -> str:
    """Get comprehensive API performance summary"""
    return """
    WITH recent_data AS (
        SELECT *
        FROM system_reliability
        WHERE timestamp >= NOW() - INTERVAL '24 hours'
    )
    SELECT 
        api_name,
        COUNT(*) as total_calls,
        AVG(latency_ms) as avg_latency,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms) as p95_latency,
        AVG(error_rate) as avg_error_rate,
        AVG(reliability_index) as avg_reliability,
        MAX(timestamp) as last_checked
    FROM recent_data
    GROUP BY api_name
    ORDER BY avg_reliability DESC
    """
