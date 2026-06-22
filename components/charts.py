import pandas as pd
import plotly.express as px
import streamlit as st


def render_rating_trend(sessions_df: pd.DataFrame) -> None:
    if sessions_df.empty:
        return
    df = sessions_df.sort_values("session_date").copy()
    df["session_date"] = pd.to_datetime(df["session_date"])
    df["avg_rating"] = pd.to_numeric(df["avg_rating"], errors="coerce")

    fig = px.line(
        df,
        x="session_date",
        y="avg_rating",
        markers=True,
        labels={"session_date": "Session Date", "avg_rating": "Avg Rating"},
        title="Rating Trend",
    )
    fig.update_yaxes(range=[0, 10])
    fig.update_traces(line_color="#6366f1", marker_color="#6366f1")
    fig.update_layout(margin=dict(t=40, b=20), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)


def render_attendance_trend(sessions_df: pd.DataFrame) -> None:
    if sessions_df.empty:
        return
    df = sessions_df.sort_values("session_date").copy()
    df["session_date"] = pd.to_datetime(df["session_date"])

    melted = df.melt(
        id_vars="session_date",
        value_vars=["batch_strength", "zoom_joined", "total_responses"],
        var_name="Metric",
        value_name="Count",
    )
    melted["Metric"] = melted["Metric"].map({
        "batch_strength": "Batch Strength",
        "zoom_joined": "Zoom Joined",
        "total_responses": "Responses",
    })

    fig = px.bar(
        melted,
        x="session_date",
        y="Count",
        color="Metric",
        barmode="group",
        labels={"session_date": "Session Date"},
        title="Attendance & Participation",
        color_discrete_map={
            "Batch Strength": "#94a3b8",
            "Zoom Joined": "#6366f1",
            "Responses": "#22c55e",
        },
    )
    fig.update_layout(margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
