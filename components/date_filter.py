"""
Predefined Date Filter Presets Component
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Tuple, Optional

def render_date_filter(df: pd.DataFrame) -> Tuple[Optional[date], Optional[date]]:
    """
    Render predefined date filter controls (Current Month, Last 30 Days, Year To Date, All Time, Custom Range).
    Returns (start_date, end_date) tuple.
    """
    st.markdown('<div style="margin-bottom: 1.25rem;">', unsafe_allow_html=True)
    
    col_label, col_radio = st.columns([1, 4])
    with col_label:
        st.markdown(
            '<div style="font-weight: 700; font-size: 0.95rem; color: #0F172A; padding-top: 6px;">📅 Periode Tanggal:</div>',
            unsafe_allow_html=True
        )
        
    with col_radio:
        preset_option = st.radio(
            "Periode Waktu",
            options=["Current Month", "Last 30 Days", "Year To Date", "All Time", "Custom Range"],
            horizontal=True,
            index=0,
            key="main_date_preset_radio",
            label_visibility="collapsed"
        )
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate Date Range based on selected preset
    today = datetime.now().date()
    
    # Or reference latest date in dataset if data is historical
    max_data_date = df["DateOnly"].max() if not df.empty else today
    ref_today = max(today, max_data_date)
    
    if preset_option == "Current Month":
        start_date = date(ref_today.year, ref_today.month, 1)
        end_date = ref_today
    elif preset_option == "Last 30 Days":
        start_date = ref_today - timedelta(days=30)
        end_date = ref_today
    elif preset_option == "Year To Date":
        start_date = date(ref_today.year, 1, 1)
        end_date = ref_today
    elif preset_option == "All Time":
        start_date = df["DateOnly"].min() if not df.empty else date(2020, 1, 1)
        end_date = df["DateOnly"].max() if not df.empty else ref_today
    elif preset_option == "Custom Range":
        c1, c2 = st.columns(2)
        min_d = df["DateOnly"].min() if not df.empty else date(2020, 1, 1)
        max_d = df["DateOnly"].max() if not df.empty else ref_today
        with c1:
            start_date = st.date_input("Tanggal Mulai", value=min_d, min_value=min_d, max_value=max_d)
        with c2:
            end_date = st.date_input("Tanggal Akhir", value=max_d, min_value=min_d, max_value=max_d)
            
    return (start_date, end_date)
