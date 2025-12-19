import streamlit as st

from auth import login_ui
from data_access import get_backend_telemetry


st.set_page_config(page_title="Developer Dashboard", layout="wide")


def main():
    st.title("Developer / System Monitoring Dashboard")

    login_ui()
    if not st.session_state.get("authenticated"):
        st.info("Please sign in to access the dashboard.")
        return

    st.caption("Source: Logfire/OpenTelemetry export in BigQuery (read-only).")

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        day = st.text_input("Day (YYYY-MM-DD)", value="")
    with col2:
        limit = st.number_input("Rows", min_value=100, max_value=50000, value=5000, step=100)
    with col3:
        st.write("")
        st.write("Tip: leave Day blank to view latest records.")

    df = get_backend_telemetry(day=day.strip() or None, limit=int(limit))
    if df.empty:
        st.warning("No telemetry rows found.")
        return

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Spans", int(len(df)))
    k2.metric("Unique routes", int(df["url_path"].nunique()) if "url_path" in df.columns else 0)
    k3.metric(
        "Server errors",
        int(df["is_server_error [derived]"].sum()) if "is_server_error [derived]" in df.columns else 0,
    )
    if "duration_ms" in df.columns:
        k4.metric("P95 duration (ms)", round(float(df["duration_ms"].quantile(0.95)), 2))
    else:
        k4.metric("P95 duration (ms)", "—")

    st.divider()

    st.subheader("Recent requests")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Simple chart: duration by route
    if "duration_ms" in df.columns and "url_path" in df.columns:
        st.subheader("Latency by route")
        agg = (
            df.dropna(subset=["duration_ms", "url_path"])
            .groupby("url_path")["duration_ms"]
            .median()
            .sort_values(ascending=False)
            .head(25)
        )
        st.bar_chart(agg)


if __name__ == "__main__":
    main()
