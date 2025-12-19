import streamlit as st

from auth import login_ui
from db import init_database
from data_access import get_case_studies, get_users, get_sessions, get_grades


st.set_page_config(
    page_title="MIND Unified Dashboard",
    page_icon="📊",
    layout="wide",
)


def _kpi(label: str, value):
    with st.container(border=True):
        st.caption(label)
        st.subheader(value)


def main():
    st.title("MIND Unified Dashboard")

    # Auth gate
    login_ui()
    if not st.session_state.get("authenticated"):
        st.info("Please sign in to access the dashboards.")
        return

    # Read-only connectivity check
    try:
        init_database()
    except Exception as e:
        st.error(
            "Database connection failed. Ensure BigQuery secrets/environment variables are set."
        )
        st.exception(e)
        return

    # Quick overview
    col1, col2, col3, col4 = st.columns(4)
    try:
        users_df = get_users(limit=1)
        sessions_df = get_sessions(limit=1)
        grades_df = get_grades(limit=1)
        cases_df = get_case_studies()

        # Use table row counts via INFORMATION_SCHEMA for performance if needed.
        # For now we show "recent" signals that load fast.
        col1.metric("Case studies", int(len(cases_df)))
        col2.metric("Latest user", users_df.iloc[0]["student_email"] if len(users_df) else "—")
        col3.metric("Latest session", sessions_df.iloc[0]["session_id"] if len(sessions_df) else "—")
        col4.metric("Latest grade", grades_df.iloc[0]["final_score"] if len(grades_df) else "—")
    except Exception:
        st.warning(
            "Overview cards could not be computed from the current dataset permissions. "
            "You can still open individual dashboards from the left sidebar."
        )

    st.markdown(
        """
This dashboard is connected to **BigQuery (read-only)**.

Use the sidebar to access:
- Student Dashboard
- Faculty Dashboard
- Developer Dashboard
- Admin Dashboard
"""
    )


if __name__ == "__main__":
    main()
