import streamlit as st


def render_kpi_cards(session: dict) -> None:
    col1, col2, col3 = st.columns(3)

    avg_rating = session.get("avg_rating")
    batch = session.get("batch_strength")
    joined = session.get("zoom_joined")
    responses = session.get("total_responses")

    col1.metric(
        "Avg Rating",
        f"{float(avg_rating):.1f} / 10" if avg_rating is not None else "—",
    )

    join_rate = (int(joined) / int(batch) * 100) if batch and joined else None
    col2.metric(
        "Join Rate",
        f"{join_rate:.0f}%" if join_rate is not None else "—",
        help="Zoom Joined ÷ Batch Strength",
    )

    resp_rate = (int(responses) / int(joined) * 100) if joined and responses else None
    col3.metric(
        "Response Rate",
        f"{resp_rate:.0f}%" if resp_rate is not None else "—",
        help="Survey Responses ÷ Zoom Joined",
    )
