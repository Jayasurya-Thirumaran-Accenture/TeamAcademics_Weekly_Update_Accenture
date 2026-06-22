import pandas as pd
import streamlit as st


def _rating_color(rating: int | None) -> str:
    if rating is None:
        return "#94a3b8"
    if rating >= 9:
        return "#22c55e"
    if rating >= 7:
        return "#f59e0b"
    return "#ef4444"


def render_feedback_cards(responses_df: pd.DataFrame) -> None:
    if responses_df.empty:
        st.info("No feedback responses for this session.")
        return

    st.markdown(f"**{len(responses_df)} response(s)**")

    for _, row in responses_df.iterrows():
        rating = row.get("rating")
        name = row.get("respondent_name") or "Anonymous"
        reason = row.get("reason") or ""
        remarks = row.get("remarks") or ""
        color = _rating_color(rating)
        rating_label = str(int(rating)) if rating is not None else "?"

        reason_html = f"<p style='margin:6px 0 0; color:#374151'>{reason}</p>" if reason else ""
        remarks_html = (
            f"<p style='margin:4px 0 0; color:#6b7280; font-size:0.85em'><em>Remarks: {remarks}</em></p>"
            if remarks else ""
        )

        st.markdown(
            f"""
            <div style="border-left:4px solid {color}; padding:10px 16px; margin-bottom:10px;
                        background:#f8fafc; border-radius:0 6px 6px 0;">
                <span style="background:{color}; color:white; padding:2px 10px;
                             border-radius:12px; font-weight:700; font-size:0.9em;">
                    ★ {rating_label}
                </span>
                &nbsp;<strong style="color:#1e293b">{name}</strong>
                {reason_html}
                {remarks_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
