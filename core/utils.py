"""
Utility functions for MIND Unified Dashboard
Data processing, formatting, and helper functions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import streamlit as st

def format_number(value: float, decimals: int = 2) -> str:
    """Format number with thousand separators"""
    if pd.isna(value):
        return "N/A"
    return f"{value:,.{decimals}f}"

def format_percentage(value: float, decimals: int = 1) -> str:
    """Format value as percentage"""
    if pd.isna(value):
        return "N/A"
    return f"{value:.{decimals}f}%"

def format_duration(seconds: int) -> str:
    """Convert seconds to human-readable duration"""
    if pd.isna(seconds) or seconds < 0:
        return "N/A"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def calculate_improvement(attempt1_score: float, attempt2_score: float) -> float:
    """Calculate improvement between two attempts"""
    if pd.isna(attempt1_score) or pd.isna(attempt2_score):
        return np.nan
    return attempt2_score - attempt1_score

def calculate_rubric_mastery(score: float, max_score: float) -> float:
    """Calculate rubric mastery percentage"""
    if pd.isna(score) or pd.isna(max_score) or max_score == 0:
        return np.nan
    return (score / max_score) * 100

def get_performance_category(score: float) -> str:
    """Categorize performance based on score"""
    if pd.isna(score):
        return "Unknown"
    elif score >= 80:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 60:
        return "Satisfactory"
    elif score >= 50:
        return "Needs Improvement"
    else:
        return "Poor"

def get_performance_color(score: float) -> str:
    """Get color code based on performance score"""
    from theme import COLORS
    
    if pd.isna(score):
        return COLORS['text_light']
    elif score >= 80:
        return COLORS['success']
    elif score >= 70:
        return '#90C695'  # Light green
    elif score >= 60:
        return COLORS['warning']
    elif score >= 50:
        return '#FF9800'  # Orange
    else:
        return COLORS['danger']

def calculate_ces_category(ces_value: float) -> str:
    """Categorize Customer Effort Score"""
    if pd.isna(ces_value):
        return "Unknown"
    elif ces_value >= 80:
        return "Very Easy"
    elif ces_value >= 60:
        return "Easy"
    elif ces_value >= 40:
        return "Moderate"
    elif ces_value >= 20:
        return "Difficult"
    else:
        return "Very Difficult"

def categorize_environment_quality(
    noise_level: float = None,
    internet_stability: float = None,
    internet_latency: float = None
) -> str:
    """
    Categorize overall environment quality based on metrics
    
    Args:
        noise_level: Noise level (0-120 dB)
        internet_stability: Stability score (0-100)
        internet_latency: Latency in ms
        
    Returns:
        Category: "Excellent", "Good", "Fair", "Poor"
    """
    scores = []
    
    # Noise level scoring (lower is better)
    if noise_level is not None and not pd.isna(noise_level):
        if noise_level <= 40:
            scores.append(100)
        elif noise_level <= 60:
            scores.append(75)
        elif noise_level <= 80:
            scores.append(50)
        else:
            scores.append(25)
    
    # Internet stability (higher is better)
    if internet_stability is not None and not pd.isna(internet_stability):
        scores.append(internet_stability)
    
    # Internet latency (lower is better)
    if internet_latency is not None and not pd.isna(internet_latency):
        if internet_latency <= 50:
            scores.append(100)
        elif internet_latency <= 100:
            scores.append(75)
        elif internet_latency <= 200:
            scores.append(50)
        else:
            scores.append(25)
    
    if not scores:
        return "Unknown"
    
    avg_score = sum(scores) / len(scores)
    
    if avg_score >= 80:
        return "Excellent"
    elif avg_score >= 65:
        return "Good"
    elif avg_score >= 50:
        return "Fair"
    else:
        return "Poor"

def get_date_range_filter(default_days: int = 30) -> Tuple[datetime, datetime]:
    """
    Create a date range filter widget
    
    Args:
        default_days: Default number of days to look back
        
    Returns:
        Tuple of (start_date, end_date)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=default_days),
            max_value=datetime.now()
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    return datetime.combine(start_date, datetime.min.time()), \
           datetime.combine(end_date, datetime.max.time())

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is 0"""
    if pd.isna(numerator) or pd.isna(denominator) or denominator == 0:
        return default
    return numerator / denominator

def aggregate_rubric_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate rubric scores by dimension
    
    Args:
        df: DataFrame with columns: rubric_dimension, score, max_score
        
    Returns:
        Aggregated DataFrame with mastery percentages
    """
    if df.empty:
        return pd.DataFrame()
    
    agg_df = df.groupby('rubric_dimension').agg({
        'score': 'mean',
        'max_score': 'mean'
    }).reset_index()
    
    agg_df['mastery_pct'] = (agg_df['score'] / agg_df['max_score']) * 100
    return agg_df

def get_at_risk_students(df: pd.DataFrame, score_threshold: float = 50) -> pd.DataFrame:
    """
    Identify at-risk students based on performance criteria
    
    Args:
        df: DataFrame with student performance data
        score_threshold: Minimum acceptable average score
        
    Returns:
        DataFrame of at-risk students
    """
    if df.empty or 'avg_score' not in df.columns:
        return pd.DataFrame()
    
    at_risk = df[df['avg_score'] < score_threshold].copy()
    return at_risk.sort_values('avg_score')

def calculate_cohort_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate aggregate metrics for a cohort
    
    Args:
        df: DataFrame with attempt data
        
    Returns:
        Dictionary of calculated metrics
    """
    if df.empty:
        return {}
    
    metrics = {
        'total_students': df['student_id'].nunique() if 'student_id' in df.columns else 0,
        'total_attempts': len(df),
        'avg_score': df['score'].mean() if 'score' in df.columns else 0,
        'avg_duration': df['duration_seconds'].mean() if 'duration_seconds' in df.columns else 0,
        'avg_ces': df['ces_value'].mean() if 'ces_value' in df.columns else 0,
        'completion_rate': (df['state'] == 'Completed').mean() * 100 if 'state' in df.columns else 0
    }
    
    return metrics

def filter_by_date_range(df: pd.DataFrame, start_date: datetime, end_date: datetime, 
                         date_column: str = 'timestamp') -> pd.DataFrame:
    """
    Filter DataFrame by date range
    
    Args:
        df: DataFrame to filter
        start_date: Start of date range
        end_date: End of date range
        date_column: Name of the date column
        
    Returns:
        Filtered DataFrame
    """
    if df.empty or date_column not in df.columns:
        return df
    
    # Ensure date column is datetime
    df[date_column] = pd.to_datetime(df[date_column])
    
    return df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]

def create_summary_stats(df: pd.DataFrame, metric_column: str) -> Dict[str, float]:
    """
    Create summary statistics for a metric
    
    Args:
        df: DataFrame
        metric_column: Column to analyze
        
    Returns:
        Dictionary with min, max, mean, median, std
    """
    if df.empty or metric_column not in df.columns:
        return {}
    
    return {
        'min': df[metric_column].min(),
        'max': df[metric_column].max(),
        'mean': df[metric_column].mean(),
        'median': df[metric_column].median(),
        'std': df[metric_column].std(),
        'count': df[metric_column].count()
    }

def get_trend_indicator(current: float, previous: float) -> str:
    """
    Get trend indicator emoji based on comparison
    
    Args:
        current: Current value
        previous: Previous value
        
    Returns:
        Emoji indicator
    """
    if pd.isna(current) or pd.isna(previous):
        return "➖"
    
    if current > previous:
        return "📈"
    elif current < previous:
        return "📉"
    else:
        return "➖"

def calculate_percentile_rank(value: float, series: pd.Series) -> float:
    """Calculate percentile rank of a value in a series"""
    if pd.isna(value) or series.empty:
        return np.nan
    
    return (series < value).sum() / len(series) * 100
