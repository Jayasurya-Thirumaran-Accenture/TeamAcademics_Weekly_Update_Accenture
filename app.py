import streamlit as st
from utils.queries import get_active_programs, get_sessions, get_responses
from components.kpi_cards import render_kpi_cards
from components.charts import render_rating_trend, render_attendance_trend
from components.feedback import render_feedback_cards
from components.session_selector import render_session_selector
from components.upload import render_upload_section
from components.program_manager import render_program_manager

st.set_page_config(
    page_title="TalentSprint Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 TalentSprint Program Dashboard")

programs = get_active_programs()

if not programs:
    st.info(
        "No programs configured yet. Open the **Admin** section below "
        "and add your first program."
    )
else:
    tab_labels = [p["short_name"] for p in programs]
    tabs = st.tabs(tab_labels)

    for tab, program in zip(tabs, programs):
        with tab:
            sessions_df = get_sessions(program["id"])

            if sessions_df.empty:
                st.info(
                    f"No session data yet for **{program['short_name']}**. "
                    "Upload the first session using the Admin section below."
                )
            else:
                recent = sessions_df.head(2).to_dict("records")

                # Show up to 2 most recent sessions side by side
                cols = st.columns(len(recent))
                for col, session in zip(cols, recent):
                    with col:
                        instructor_part = f" · {session['instructor']}" if session.get("instructor") else ""
                        st.markdown(
                            f"**{session.get('topic', 'Session')}**"
                            f"  \n{session.get('session_date', '—')}{instructor_part}"
                        )
                        render_kpi_cards(session)

                st.divider()

                col_left, col_right = st.columns(2)
                with col_left:
                    render_rating_trend(sessions_df)
                with col_right:
                    render_attendance_trend(sessions_df)

                st.divider()

                selected_session_id = render_session_selector(
                    sessions_df, key=f"session_sel_{program['id']}"
                )
                if selected_session_id:
                    responses_df = get_responses(selected_session_id)
                    render_feedback_cards(responses_df)

# Admin section — password protected
st.divider()
with st.expander("⚙ Admin", expanded=False):
    pwd = st.text_input("Admin password", type="password", key="admin_pwd")
    if pwd:
        if pwd == st.secrets.get("admin", {}).get("password", ""):
            admin_tab_upload, admin_tab_programs = st.tabs(["Upload Session Data", "Manage Programs"])
            with admin_tab_upload:
                render_upload_section()
            with admin_tab_programs:
                render_program_manager()
        else:
            st.error("Incorrect password.")
