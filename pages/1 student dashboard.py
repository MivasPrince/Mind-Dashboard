"""
Student Dashboard - Personal Learning Analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from core.db import get_bigquery_client, run_query
from core.settings import get_table_ref, COLORS

# Page config MUST be first
st.set_page_config(
    page_title="Student Dashboard - MIND",
    page_icon="📚",
    layout="wide"
)

# Initialize session state if not exists
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None

# Check authentication
if not st.session_state.authenticated:
    st.warning("⚠️ Please log in from the Home page")
    st.stop()

# Header
st.markdown("# 📚 Student Dashboard")
st.markdown(f"### Welcome, {st.session_state.username}!")
st.markdown("Track your learning journey and performance")
st.markdown("---")

client = get_bigquery_client()
if not client:
    st.error("❌ Failed to connect to database")
    st.stop()

# Student Selector
st.markdown("### 👤 Select Student")
users_query = f"""
SELECT user_id, name, email
FROM {get_table_ref('user')}
WHERE role = 'student' OR role IS NULL
ORDER BY name LIMIT 100
"""
users_df = run_query(users_query, client)

if users_df is None or users_df.empty:
    st.warning("No students found")
    st.stop()

student_options = {f"{row['name']} ({row['email']})": row['user_id'] 
                  for _, row in users_df.iterrows()}
selected = st.selectbox("Choose student", list(student_options.keys()))
student_id = student_options[selected]

st.divider()

# KPI GAUGES
st.markdown("### 📊 Your Performance Metrics")

cases_q = f"SELECT COUNT(DISTINCT case_study) as val FROM {get_table_ref('grades')} WHERE user = '{student_id}'"
cases_df = run_query(cases_q, client)
cases = int(cases_df['val'].iloc[0]) if cases_df is not None and not cases_df.empty else 0

score_q = f"SELECT AVG(final_score) as val FROM {get_table_ref('grades')} WHERE user = '{student_id}'"
score_df = run_query(score_q, client)
avg_score = float(score_df['val'].iloc[0]) if score_df is not None and not score_df.empty else 0

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure(go.Indicator(
        mode="number+gauge",
        value=cases,
        title={'text': "📚 Cases Attempted"},
        gauge={'axis': {'range': [0, 10]}, 'bar': {'color': COLORS['primary']}}
    ))
    fig.update_layout(height=200)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure(go.Indicator(
        mode="number+gauge",
        value=avg_score,
        title={'text': "📈 Average Score"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': COLORS['success']}}
    ))
    fig.update_layout(height=200)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# PERFORMANCE TREND
st.markdown("### 📈 Performance Trend")

perf_q = f"""
SELECT DATE(timestamp) as date, final_score as score
FROM {get_table_ref('grades')}
WHERE user = '{student_id}'
ORDER BY timestamp
"""
perf_data = run_query(perf_q, client)

if perf_data is not None and not perf_data.empty:
    fig = px.line(perf_data, x='date', y='score', markers=True, title="Your Progress Over Time")
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Passing Threshold")
    fig.update_traces(line_color=COLORS['primary'], line_width=3)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No performance data available yet")

st.divider()

# RUBRIC RADAR
st.markdown("### 🎯 Skills Analysis")

rubric_q = f"""
SELECT 
    AVG(individual_scores.communication) as comm,
    AVG(individual_scores.comprehension) as comp,
    AVG(individual_scores.critical_thinking) as crit
FROM {get_table_ref('grades')}
WHERE user = '{student_id}'
"""
rubric_data = run_query(rubric_q, client)

if rubric_data is not None and not rubric_data.empty:
    comm = float(rubric_data['comm'].iloc[0] or 0)
    comp = float(rubric_data['comp'].iloc[0] or 0)
    crit = float(rubric_data['crit'].iloc[0] or 0)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[comm, comp, crit, comm],
            theta=['Communication', 'Comprehension', 'Critical Thinking', 'Communication'],
            fill='toself',
            line_color=COLORS['primary']
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            height=400,
            title="Your Rubric Scores"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Average Scores")
        st.metric("Communication", f"{comm:.1f}")
        st.metric("Comprehension", f"{comp:.1f}")
        st.metric("Critical Thinking", f"{crit:.1f}")

st.caption("💡 Continue learning and track your progress!")
