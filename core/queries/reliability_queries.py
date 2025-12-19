import pandas as pd
from typing import Optional
# Assuming db.py is one level up (in core/)
from db import run_query 


# ----------------- BASIC LOADERS -----------------

def load_system_reliability(start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    """
    Full reliability logs filtered by an optional date range.
    """
    sql = """
        SELECT *
        FROM system_reliability
        WHERE timestamp >= :start AND timestamp <= :end
        ORDER BY timestamp;
    """
    
    # Prepare parameters with safe default date range
    params = {
        "start": f"{start_date} 00:00:00" if start_date else "1900-01-01 00:00:00",
        "end": f"{end_date} 23:59:59" if end_date else "2999-12-31 23:59:59"
    }
    
    return run_query(sql, params)


def load_latest_reliability() -> pd.DataFrame:
    """
    Latest reliability readings (useful for KPI tiles).
    """
    sql = """
        SELECT *
        FROM system_reliability
        ORDER BY timestamp DESC
        LIMIT 20;
    """
    return run_query(sql)


# ----------------- AGGREGATES -----------------

def load_api_latency_summary(start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    """
    Calculates average, P50, and P95 latency per API, filtered by date.
    """
    sql = """
        SELECT
            api_name,
            AVG(latency_ms)::numeric(10,2) AS avg_latency,
            PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY latency_ms)::numeric(10,2) AS p50_latency,
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms)::numeric(10,2) AS p95_latency,
            COUNT(id) AS total_pings
        FROM system_reliability
        WHERE timestamp >= :start AND timestamp <= :end
        GROUP BY api_name
        ORDER BY avg_latency DESC;
    """
    
    # Prepare parameters with safe default date range
    params = {
        "start": f"{start_date} 00:00:00" if start_date else "1900-01-01 00:00:00",
        "end": f"{end_date} 23:59:59" if end_date else "2999-12-31 23:59:59"
    }

    # Added explicit CASTs for percentiles and filtered by date
    return run_query(sql, params)


def load_error_rate_by_api(start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    """
    Calculates the average error rate per API, filtered by date.
    """
    sql = """
        SELECT
            api_name,
            AVG(error_rate)::numeric(10,4) AS avg_error_rate,
            SUM(CASE WHEN error_rate > 0 THEN 1 ELSE 0 END) AS incidents_count
        FROM system_reliability
        WHERE timestamp >= :start AND timestamp <= :end
        GROUP BY api_name
        ORDER BY avg_error_rate DESC;
    """
    
    # Prepare parameters with safe default date range
    params = {
        "start": f"{start_date} 00:00:00" if start_date else "1900-01-01 00:00:00",
        "end": f"{end_date} 23:59:59" if end_date else "2999-12-31 23:59:59"
    }
    # Added incidents_count and date filtering
    return run_query(sql, params)


def load_critical_incidents() -> pd.DataFrame:
    """
    Loads all critical incidents (no date filtering, assume this is a retrospective log).
    """
    sql = """
        SELECT *
        FROM system_reliability
        WHERE severity = 'Critical'
        ORDER BY timestamp DESC;
    """
    return run_query(sql)


def load_incidents_by_location() -> pd.DataFrame:
    """
    Counts the number of Critical incidents by recorded location.
    """
    sql = """
        SELECT 
            location,
            COUNT(*) AS critical_incidents
        FROM system_reliability
        WHERE severity = 'Critical'
        GROUP BY location
        ORDER BY critical_incidents DESC;
    """
    return run_query(sql)
