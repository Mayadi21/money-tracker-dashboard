"""
Sidebar category and search filter controls component
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any
from utils.constants import TYPE_INCOME, TYPE_EXPENSE

def render_sidebar(df: pd.DataFrame) -> Dict[str, Any]:
    """Render collapsible sidebar with transaction type, category selection, and search query."""
    with st.sidebar:
        st.markdown("### ⚙️ Filter & pencarian")
        st.markdown("---")
        
        if df.empty:
            st.warning("Dataframe kosong.")
            return {}

        # Reset button handler
        if st.button("🔄 Reset Filter", use_container_width=True):
            st.session_state["filter_type"] = "All"
            st.session_state["filter_categories"] = []
            st.session_state["filter_search"] = ""
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)

        # 1. Transaction Type Filter
        type_options = ["All", TYPE_INCOME, TYPE_EXPENSE]
        selected_type = st.selectbox(
            "Tipe Transaksi",
            options=type_options,
            index=type_options.index(st.session_state.get("filter_type", "All"))
        )

        # 2. Category Filter
        available_categories = sorted(df["Kategori"].unique().tolist())
        selected_categories = st.multiselect(
            "Filter Kategori",
            options=available_categories,
            default=st.session_state.get("filter_categories", [])
        )

        # 3. Search Filter
        search_query = st.text_input(
            "Cari Transaksi",
            value=st.session_state.get("filter_search", ""),
            placeholder="Kata kunci catatan / kategori..."
        )

        st.markdown("---")
        st.caption(f"📊 Total Dataset: {len(df):,} baris")

        return {
            "type": selected_type,
            "categories": selected_categories,
            "search": search_query
        }
