import streamlit as st

from auth import login_ui
from data_access import get_case_studies, get_grades, get_users


st.set_page_config(page_title="Faculty Dashboard", layout="wide")


def main():
    st.title("Faculty Dashboard")

    login_ui()
    if not st.session_state.get("authenticated"):
        st.info("Please sign in to access the dashboard.")
        return

    users = get_users(limit=20000)
    grades = get_grades(limit=200000)
    cases = get_case_studies()

    if grades.empty:
        st.warning("No grades data found.")
        return

    # Filters
    left, right = st.columns([2, 3])
    with left:
        dept = st.selectbox(
            "Department", options=["All"] + sorted(users["department"].dropna().unique().tolist())
        )
        cohort = st.selectbox(
            "Cohort", options=["All"] + sorted(users["cohort"].dropna().unique().tolist())
        )
    with right:
        case_opts = ["All"] + [f"{r['title']} ({r['case_study_id']})" for _, r in cases.iterrows()]
        case_choice = st.selectbox("Case study", options=case_opts)

    # Apply filters via joins
    g = grades.copy()
    if not users.empty:
        g = g.merge(users[["user_id", "department", "cohort"]], on="user_id", how="left")
    if dept != "All":
        g = g[g["department"] == dept]
    if cohort != "All":
        g = g[g["cohort"] == cohort]
    if case_choice != "All":
        case_id = case_choice.split("(")[-1].rstrip(")")
        g = g[g["case_study_id"].astype(str) == case_id]

    st.subheader("Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Grade records", int(len(g)))
    c2.metric("Students", int(g["user_id"].nunique()))
    c3.metric("Average final score", round(float(g["final_score"].mean()), 2) if len(g) else 0)

    st.divider()

    st.subheader("Performance distribution")
    if "performance_band [derived]" in g.columns:
        band_counts = g["performance_band [derived]"].value_counts().sort_index()
        st.bar_chart(band_counts)
    else:
        st.info("Derived performance band column not present in the dataset.")

    st.divider()
    st.subheader("Grades table")
    st.dataframe(g.sort_values("timestamp", ascending=False), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
