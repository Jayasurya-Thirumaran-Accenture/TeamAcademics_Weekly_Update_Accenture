from __future__ import annotations
import streamlit as st
from utils.queries import get_all_programs, add_program, update_program


def render_program_manager() -> None:
    st.subheader("Manage Programs")
    programs = get_all_programs()

    if programs:
        for prog in programs:
            pid = prog["id"]
            status_icon = "🟢" if prog["active"] else "⚫"
            with st.expander(
                f"{status_icon} {prog['short_name']} — {prog['full_name']}",
                expanded=False,
            ):
                edit_key = f"edit_mode_{pid}"

                if st.session_state.get(edit_key):
                    new_short = st.text_input("Short name", value=prog["short_name"], key=f"sn_{pid}")
                    new_full = st.text_input("Full name", value=prog["full_name"], key=f"fn_{pid}")
                    new_order = st.number_input(
                        "Display order", value=int(prog["display_order"]),
                        min_value=1, key=f"ord_{pid}"
                    )
                    col_save, col_cancel = st.columns(2)
                    if col_save.button("Save changes", key=f"save_{pid}", type="primary"):
                        update_program(pid, {
                            "short_name": new_short.strip(),
                            "full_name": new_full.strip(),
                            "display_order": int(new_order),
                        })
                        st.session_state[edit_key] = False
                        st.success(f"Updated: {new_short}")
                        st.rerun()
                    if col_cancel.button("Cancel", key=f"cancel_{pid}"):
                        st.session_state[edit_key] = False
                        st.rerun()

                else:
                    col_edit, col_toggle, col_order = st.columns([1, 1, 1])

                    if col_edit.button("Edit", key=f"edit_{pid}"):
                        st.session_state[edit_key] = True
                        st.rerun()

                    toggle_label = "Deactivate" if prog["active"] else "Reactivate"
                    if col_toggle.button(toggle_label, key=f"toggle_{pid}"):
                        update_program(pid, {"active": not prog["active"]})
                        st.rerun()

                    new_order = col_order.number_input(
                        "Order",
                        value=int(prog["display_order"]),
                        min_value=1,
                        key=f"qord_{pid}",
                        label_visibility="collapsed",
                        help="Display order (lower = leftmost tab)",
                    )
                    if int(new_order) != int(prog["display_order"]):
                        update_program(pid, {"display_order": int(new_order)})
                        st.rerun()

    st.divider()
    st.markdown("**Add New Program**")
    with st.form("add_program_form", clear_on_submit=True):
        short_name = st.text_input("Short name", placeholder="e.g. ADSML C10")
        full_name = st.text_input("Full name", placeholder="e.g. Advanced Programme in Data Science")
        cohort = st.number_input("Cohort number", min_value=1, value=1)
        display_order = st.number_input("Display order", min_value=1, value=len(programs) + 1)
        submitted = st.form_submit_button("Add Program", type="primary")

    if submitted:
        if not short_name.strip():
            st.error("Short name is required.")
        elif short_name.strip() in [p["short_name"] for p in programs]:
            st.error(f"A program named '{short_name.strip()}' already exists.")
        else:
            add_program({
                "short_name": short_name.strip(),
                "full_name": full_name.strip(),
                "cohort": int(cohort),
                "display_order": int(display_order),
                "active": True,
            })
            st.success(f"Added program: {short_name.strip()}")
            st.rerun()
