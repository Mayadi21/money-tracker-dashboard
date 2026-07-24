"""
Redesigned Premium Monthly Summary Card Component
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.formatter import format_currency
from utils.constants import TYPE_INCOME, TYPE_EXPENSE

def render_monthly_summary_card(df: pd.DataFrame):
    """
    Render clean, premium finance summary card using native Streamlit UI elements (No raw HTML leaks!).
    """
    st.markdown('<div class="fin-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin-bottom: 1rem;">🗓️ Ringkasan Ringkas Finansial</h3>', unsafe_allow_html=True)
    
    if df.empty:
        st.info("Tidak ada data transaksi untuk ringkasan bulan ini.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
        
    inc_df = df[df["Jenis"] == TYPE_INCOME]
    exp_df = df[df["Jenis"] == TYPE_EXPENSE]
    
    total_inc = inc_df["Jumlah"].sum() if not inc_df.empty else 0.0
    total_exp = exp_df["Jumlah"].sum() if not exp_df.empty else 0.0
    net_cashflow = total_inc - total_exp
    
    # Largest Expense Category
    if not exp_df.empty and total_exp > 0:
        top_exp_series = exp_df.groupby("Kategori")["Jumlah"].sum()
        top_exp_cat = top_exp_series.idxmax()
        top_exp_val = top_exp_series.max()
        top_exp_pct = (top_exp_val / total_exp) * 100
        top_exp_str = f"{top_exp_cat} ({top_exp_pct:.1f}%)"
    else:
        top_exp_str = "Tidak Ada"

    # Largest Income Category
    if not inc_df.empty and total_inc > 0:
        top_inc_series = inc_df.groupby("Kategori")["Jumlah"].sum()
        top_inc_cat = top_inc_series.idxmax()
        top_inc_val = top_inc_series.max()
        top_inc_pct = (top_inc_val / total_inc) * 100
        top_inc_str = f"{top_inc_cat} ({top_inc_pct:.1f}%)"
    else:
        top_inc_str = "Tidak Ada"

    # Render Streamlit Metrics Grid
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Pemasukan (Income)", format_currency(total_inc))
    with c2:
        st.metric("Pengeluaran (Expense)", format_currency(total_exp))
    with c3:
        st.metric("Arus Kas Bersih (Net Cash Flow)", format_currency(net_cashflow), delta=f"{'+' if net_cashflow>=0 else ''}{format_currency(net_cashflow, compact=True)}")
        
    st.divider()
    
    c_cat1, c_cat2 = st.columns(2)
    with c_cat1:
        st.caption("🔴 Kategori Pengeluaran Terbesar")
        st.subheader(top_exp_str)
    with c_cat2:
        st.caption("🟢 Kategori Pemasukan Terbesar")
        st.subheader(top_inc_str)
        
    st.markdown('</div>', unsafe_allow_html=True)
