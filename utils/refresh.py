"""
Dashboard state refresh and timestamp management utilities
"""
from datetime import datetime
import streamlit as st


def init_refresh_state():
    """Initialize last refreshed timestamp in session state if not already present."""
    if "last_refreshed_at" not in st.session_state:
        st.session_state["last_refreshed_at"] = datetime.now()
    if "show_refresh_success" not in st.session_state:
        st.session_state["show_refresh_success"] = False


def refresh_dashboard():
    """
    Clear cache, update refresh timestamp, set notification flag, and rerun Streamlit app.
    """
    with st.spinner("Refreshing dashboard..."):
        # Clear Streamlit data caches
        st.cache_data.clear()
        if hasattr(st, "cache_resource"):
            st.cache_resource.clear()

        # Update refresh timestamp & notification state
        st.session_state["last_refreshed_at"] = datetime.now()
        st.session_state["show_refresh_success"] = True

        # Trigger Streamlit app rerun
        st.rerun()


def get_last_refresh_str() -> tuple:
    """
    Return formatted (date_str, time_str) for the last refresh timestamp.
    Example: ("24 Jul 2026", "14:38:12")
    """
    init_refresh_state()
    dt = st.session_state.get("last_refreshed_at", datetime.now())
    date_str = dt.strftime("%d %b %Y")
    time_str = dt.strftime("%H:%M:%S")
    return date_str, time_str


def render_refresh_notification():
    """Display temporary success notification if dashboard was just refreshed."""
    if st.session_state.get("show_refresh_success", False):
        st.toast("✅ Dashboard updated successfully.")
        st.session_state["show_refresh_success"] = False
