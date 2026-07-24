"""
Financial Deep-Dive Analytics & Behavioral Spending Component
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any
from utils.formatter import format_currency, format_percent, get_trend_indicator
from utils.statistics import get_transaction_extremes, analyze_spending_behavior, compute_monthly_summary

def render_analytics_tab(df: pd.DataFrame, kpis: Dict[str, Any]):
    """Render full Financial Analytics & Behavioral Spending Analysis views."""
    if df.empty:
        st.info("Tidak ada data untuk analisis.")
        return
        
    st.subheader("📊 Analisis Keuangan & Perilaku Pengeluaran")
    
    extremes = get_transaction_extremes(df)
    behavior = analyze_spending_behavior(df)
    monthly_df = compute_monthly_summary(df)
    
    # 1. Transaction Extremes Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="fin-card">
                <div class="metric-title">Transaksi Terbesar</div>
                <div class="metric-value" style="color: #2563EB;">{format_currency(extremes['largest_tx'])}</div>
                <div class="metric-subtitle">Nominal tunggal tertinggi</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="fin-card">
                <div class="metric-title">Transaksi Terkecil</div>
                <div class="metric-value" style="color: #64748B;">{format_currency(extremes['smallest_tx'])}</div>
                <div class="metric-subtitle">Nominal tunggal terendah</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="fin-card">
                <div class="metric-title">Rata-Rata Transaksi</div>
                <div class="metric-value" style="color: #0F172A;">{format_currency(extremes['avg_tx'])}</div>
                <div class="metric-subtitle">Nilai rerata per transaksi</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Behavioral Spending Breakdown
    st.markdown('<div class="fin-card">', unsafe_allow_html=True)
    st.markdown('<div class="fin-card-title">🔍 Profil Perilaku Pengeluaran</div>', unsafe_allow_html=True)
    
    b_col1, b_col2 = st.columns(2)
    
    with b_col1:
        most_exp_cat, most_exp_cat_amt = behavior["most_expensive_category"]
        least_exp_cat, least_exp_cat_amt = behavior["least_expensive_category"]
        most_act_cat, most_act_cat_cnt = behavior["most_active_category"]
        
        st.markdown(f"• **Kategori Terboros:** {most_exp_cat} ({format_currency(most_exp_cat_amt)})")
        st.markdown(f"• **Kategori Terhemat:** {least_exp_cat} ({format_currency(least_exp_cat_amt)})")
        st.markdown(f"• **Kategori Tersering:** {most_act_cat} ({most_act_cat_cnt} transaksi)")
        
    with b_col2:
        most_exp_day, most_exp_day_amt = behavior["most_expensive_day"]
        most_act_day, most_act_day_cnt = behavior["most_active_day"]
        no_exp_streak = behavior["streak_without_expenses"]
        exp_streak = behavior["streak_with_expenses"]
        
        st.markdown(f"• **Hari Terboros:** {most_exp_day} ({format_currency(most_exp_day_amt)})")
        st.markdown(f"• **Hari Tersering:** {most_act_day} ({most_act_day_cnt} kali belanja)")
        st.markdown(f"• **Rekor Bebas Belanja:** {no_exp_streak} Hari Berturut-turut")
        st.markdown(f"• **Streak Pengeluaran:** {exp_streak} Hari Berturut-turut")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. Monthly Financial Report Table
    st.subheader("📅 Laporan Ringkasan Bulanan")
    if not monthly_df.empty:
        report_df = monthly_df.copy()
        report_df["Indicator"] = report_df["Growth%"].apply(lambda g: get_trend_indicator(g)[0])
        report_df["Formatted_Pemasukan"] = report_df["Pemasukan"].apply(lambda v: format_currency(v))
        report_df["Formatted_Pengeluaran"] = report_df["Pengeluaran"].apply(lambda v: format_currency(v))
        report_df["Formatted_Saldo"] = report_df["Saldo"].apply(lambda v: format_currency(v))
        report_df["Formatted_SavingsRate"] = report_df["SavingsRate"].apply(lambda v: f"{v:.1f}%")
        report_df["Formatted_Growth"] = report_df.apply(
            lambda r: f"{r['Indicator']} {r['Growth%']:+.1f}%", axis=1
        )
        
        display_df = report_df[[
            "YearMonth", "Formatted_Pemasukan", "Formatted_Pengeluaran",
            "Formatted_Saldo", "Formatted_SavingsRate", "Formatted_Growth"
        ]].rename(columns={
            "YearMonth": "Bulan",
            "Formatted_Pemasukan": "Pemasukan",
            "Formatted_Pengeluaran": "Pengeluaran",
            "Formatted_Saldo": "Saldo Bersih",
            "Formatted_SavingsRate": "Savings Rate",
            "Formatted_Growth": "Pertumbuhan Pengeluaran"
        })
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
