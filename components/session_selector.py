import pandas as pd
import streamlit as st


def render_session_selector(sessions_df: pd.DataFrame, key: str) -> str | None:
    if sessions_df.empty:
        return None

    sorted_df = sessions_df.sort_values("session_date", ascending=False)
    options: dict[str, str] = {}
    for _, row in sorted_df.iterrows():
        topic = row.get("topic") or "Session"
        label = f"{row['session_date']}  —  {topic}"
        options[label] = row["id"]

    selected_label = st.selectbox("View feedback for session:", list(options.keys()), key=key)
    return options.get(selected_label)
