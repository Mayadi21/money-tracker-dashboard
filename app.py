"""
Money Tracker Dashboard - Modern Personal Finance Application
Reorganized layout hierarchy: Date Presets -> KPIs (Income, Expense, Net Cash Flow) -> Hero Trend Chart -> Dual Donuts -> Transactions
"""
import streamlit as st

# 1. Page Configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="Money Tracker - Finance Dashboard",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports after page_config
import pandas as pd
from utils.helpers import load_css, render_empty_state
from utils.data_loader import load_data
from utils.filters import filter_dataframe
from components.header import render_header
from components.date_filter import render_date_filter
from components.metric_cards import render_primary_kpi_cards
from components.cashflow_chart import render_cashflow_hero_chart
from components.donut_charts import render_dual_donut_charts
from components.transaction_table import render_transaction_table
from components.sidebar import render_sidebar

def main():
    # 2. Inject CSS & Theme Tokens
    load_css("assets/styles.css")

    # ---------------------------------------------------
    # 1. HEADER
    # ---------------------------------------------------
    render_header(
        title="💸 Dashboard Keuangan",
        subtitle="Aplikasi Keuangan Pribadi - Evaluasi Pemasukan, Pengeluaran & Arus Kas"
    )

    # Load Cached Data
    with st.spinner("🔄 Memuat data transaksi..."):
        raw_df = load_data()

    if raw_df.empty:
        st.error("Data tidak ditemukan atau format data tidak valid.")
        return

    # Render Sidebar Filter Controls (Type, Category, Search)
    sidebar_params = render_sidebar(raw_df)

    # ---------------------------------------------------
    # 2. DATE FILTER PRESETS CONTROL
    # ---------------------------------------------------
    start_date, end_date = render_date_filter(raw_df)

    # Apply Active Filters (Date Preset + Sidebar Filters)
    filtered_df = filter_dataframe(
        raw_df,
        date_range=(start_date, end_date) if (start_date and end_date) else None,
        tx_type=sidebar_params.get("type", "All"),
        categories=sidebar_params.get("categories"),
        search_query=sidebar_params.get("search", "")
    )

    # Handle empty filter state gracefully
    if filtered_df.empty:
        render_empty_state("Tidak ada transaksi yang cocok dengan periode dan filter yang Anda pilih.")
        return

    # ---------------------------------------------------
    # 3. PRIMARY KPI CARDS
    #    (Total Income | Total Expense | Net Cash Flow)
    # ---------------------------------------------------
    render_primary_kpi_cards(filtered_df)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # 4. HERO SECTION: KUMULATIF PEMASUKAN VS PENGELUARAN
    #    (Aggregation Level: Daily | Weekly | Monthly)
    # ---------------------------------------------------
    render_cashflow_hero_chart(filtered_df)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # 5. DUAL DONUT CHARTS (Side-by-Side)
    #    Left: Income Distribution ("Where does my income come from?")
    #    Right: Expense Distribution ("Where does my money go?")
    # ---------------------------------------------------
    render_dual_donut_charts(filtered_df)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # 6. RECENT TRANSACTIONS TABLE
    # ---------------------------------------------------
    render_transaction_table(filtered_df)

if __name__ == "__main__":
    main()