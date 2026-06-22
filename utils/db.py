import streamlit as st
from supabase import create_client, Client


def get_client() -> Client:
    if "supabase_client" not in st.session_state:
        try:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
        except KeyError:
            st.error(
                "Supabase credentials not configured. "
                "Add [supabase] url and key to your Streamlit secrets. "
                "See README.md for setup instructions."
            )
            st.stop()
        st.session_state.supabase_client = create_client(url, key)
    return st.session_state.supabase_client
