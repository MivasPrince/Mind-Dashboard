import streamlit as st

from auth import login_ui
from data_access import (
    get_case_studies,
    get_conversations,
    get_grades,
    get_sessions,
    get_users,
)


st.set_page_config(page_title="Student Dashboard", layout="wide")


def main():
    st.title("Student Dashboard")

    login_ui()
    if not st.session_state.get("authenticated"):
        st.info("Please sign in to access the dashboard.")
        return

    users = get_users(limit=5000)
    if users.empty:
        st.warning("No users found in BigQuery dataset.")
        return

    # Select student by email
    email = st.selectbox(
        "Select student", options=sorted(users["student_email"].dropna().unique())
    )
    user_row = users[users["student_email"] == email].iloc[0]
    user_id = str(user_row["user_id"])

    st.subheader("Profile")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Name", user_row.get("name") or "—")
    c2.metric("Role", user_row.get("role") or "—")
    c3.metric("Department", user_row.get("department") or "—")
    c4.metric("Cohort", user_row.get("cohort") or "—")

    st.divider()

    # Sessions
    st.subheader("Sessions")
    sessions = get_sessions(user_id=user_id, limit=2000)
    st.dataframe(sessions, use_container_width=True, hide_index=True)

    st.divider()

    # Grades
    st.subheader("Grades")
    grades = get_grades(user_id=user_id, limit=5000)
    if grades.empty:
        st.info("No grades found for this user.")
    else:
        st.dataframe(grades, use_container_width=True, hide_index=True)

        # Trend chart
        trend = grades[["timestamp", "final_score"]].dropna()
        if not trend.empty:
            trend = trend.sort_values("timestamp")
            st.line_chart(trend.set_index("timestamp")["final_score"])

    st.divider()

    # Conversations (optional filter by case study)
    st.subheader("Conversations")
    cases = get_case_studies()
    case_map = {
        f"{r['title']} ({r['case_study_id']})": r["case_study_id"]
        for _, r in cases.iterrows()
    }
    choice = st.selectbox("Filter by case study (optional)", options=["All"] + list(case_map.keys()))
    case_id = None if choice == "All" else case_map[choice]

    conv = get_conversations(case_study_id=case_id, user_id=user_id, limit=500)
    st.dataframe(conv, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
