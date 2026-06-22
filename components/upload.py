from __future__ import annotations
import streamlit as st
from utils.parser import parse_session_excel
from utils.queries import get_active_programs, session_exists, upsert_session, insert_responses

CONFIDENCE_THRESHOLD = 0.4


def render_upload_section() -> None:
    st.subheader("Upload New Session Data")
    uploaded = st.file_uploader(
        "Drop Zoom session Excel file here (.xlsx)",
        type=["xlsx"],
        key="session_upload",
    )

    if uploaded is None:
        return

    programs = get_active_programs()
    if not programs:
        st.error("No active programs configured. Add a program in the Manage Programs tab first.")
        return

    try:
        file_bytes = uploaded.read()
        parsed = parse_session_excel(file_bytes, programs)
    except ValueError as e:
        st.error(str(e))
        return

    meta = parsed["metadata"]
    responses = parsed["responses"]
    matched_id = parsed["matched_program_id"]
    confidence = parsed["match_confidence"]

    program_options = {p["short_name"]: p["id"] for p in programs}

    # Program selection
    if confidence >= CONFIDENCE_THRESHOLD and matched_id:
        matched_name = next((p["short_name"] for p in programs if p["id"] == matched_id), None)
        st.info(f"Auto-detected program: **{matched_name}** (confidence {confidence:.0%})")
        selected_program_id = matched_id
        if st.checkbox("Override program selection", key="override_program"):
            chosen = st.selectbox("Select program", list(program_options.keys()), key="manual_program")
            selected_program_id = program_options[chosen]
    else:
        st.warning("Could not auto-detect program from this file. Please select manually.")
        chosen = st.selectbox("Select program", list(program_options.keys()), key="manual_program")
        selected_program_id = program_options[chosen]

    # Preview
    st.markdown("#### Session Preview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Topic", meta["topic"] or "—")
    c2.metric("Date", meta["session_date"] or "—")
    c3.metric("Avg Rating", f"{meta['avg_rating']}/10" if meta["avg_rating"] else "—")
    c4.metric("Responses", meta["total_responses"])

    if meta.get("instructor"):
        st.caption(f"Instructor: {meta['instructor']}")

    # Duplicate check
    existing = session_exists(selected_program_id, meta["session_date"], meta["topic"])
    if existing:
        st.warning(
            f"A session already exists for this program on **{meta['session_date']}** "
            f"({meta['topic']}). Saving will overwrite it."
        )

    if st.button("Save Session Data", type="primary", key="save_session"):
        session_data = {
            "program_id": selected_program_id,
            "topic": meta["topic"],
            "session_date": meta["session_date"],
            "session_time": meta["session_time"],
            "instructor": meta["instructor"],
            "batch_strength": meta["batch_strength"],
            "zoom_joined": meta["zoom_joined"],
            "total_responses": meta["total_responses"],
            "avg_rating": meta["avg_rating"],
        }
        with st.spinner("Saving to database..."):
            session_id = upsert_session(session_data)
            insert_responses(session_id, responses)
        st.success(
            f"Saved: **{meta['topic']}** on {meta['session_date']} — "
            f"{meta['total_responses']} responses, avg rating {meta['avg_rating']}/10"
        )
        st.rerun()
