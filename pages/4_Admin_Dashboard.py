import streamlit as st

from auth import login_ui
from data_access import get_web_events, get_web_sessions


st.set_page_config(page_title="Admin Dashboard", layout="wide")


def main():
    st.title("Administrative Dashboard")

    login_ui()
    if not st.session_state.get("authenticated"):
        st.info("Please sign in to access the dashboard.")
        return

    st.caption("Source: PostHog exports in BigQuery (read-only).")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        email = st.text_input("Filter by distinct_id (email) (optional)", value="")
    with col2:
        session_limit = st.number_input("Sessions rows", min_value=100, max_value=50000, value=5000, step=100)
    with col3:
        event_limit = st.number_input("Events rows", min_value=100, max_value=50000, value=5000, step=100)

    sessions = get_web_sessions(distinct_id=email.strip() or None, limit=int(session_limit))
    events = get_web_events(distinct_id=email.strip() or None, limit=int(event_limit))

    st.subheader("Web sessions")
    if sessions.empty:
        st.warning("No web sessions found.")
    else:
        k1, k2, k3 = st.columns(3)
        k1.metric("Sessions", int(len(sessions)))
        if "session_duration" in sessions.columns:
            k2.metric("Avg session duration (s)", round(float(sessions["session_duration"].mean()), 2))
        else:
            k2.metric("Avg session duration (s)", "—")
        if "is_bounce" in sessions.columns:
            k3.metric("Bounce rate", f"{round(100*float(sessions['is_bounce'].mean()), 2)}%")
        else:
            k3.metric("Bounce rate", "—")
        st.dataframe(sessions, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("Web events")
    if events.empty:
        st.warning("No web events found.")
        return

    k4, k5, k6 = st.columns(3)
    k4.metric("Events", int(len(events)))
    if "is_exception_event [derived]" in events.columns:
        k5.metric("Exceptions", int(events["is_exception_event [derived]"].sum()))
    else:
        k5.metric("Exceptions", "—")
    k6.metric("Unique users", int(events["distinct_id"].nunique()) if "distinct_id" in events.columns else 0)

    if "event" in events.columns:
        st.subheader("Top events")
        top_events = events["event"].value_counts().head(25)
        st.bar_chart(top_events)

    st.dataframe(events, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
