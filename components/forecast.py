"""
Financial Prediction & Run-rate Forecast Component
"""
import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
from typing import Dict, Any
from utils.formatter import format_currency, format_percent
from utils.constants import TYPE_EXPENSE, TYPE_INCOME

def render_forecast_section(kpis: Dict[str, Any], df: pd.DataFrame):
    """Render month-end balance, expense, and savings projection based on run-rate daily averages."""
    st.subheader("🔮 Estimasi & Proyeksi Akhir Bulan")
    st.markdown("Proyeksi berbasis rata-rata historis (run-rate) untuk membantu merencanakan keuangan Anda hingga akhir bulan.")
    
    if df.empty:
        st.info("Tidak ada data untuk proyeksi.")
        return
        
    now = datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    days_passed = max(now.day, 1)
    days_remaining = days_in_month - days_passed
    
    avg_daily_exp = kpis["avg_daily_expense"]
    avg_daily_inc = kpis["avg_daily_income"]
    
    curr_income = kpis["total_income"]
    curr_expense = kpis["total_expense"]
    
    # Run-rate estimates
    est_future_expense = avg_daily_exp * days_remaining
    est_total_monthly_expense = curr_expense + est_future_expense
    
    est_future_income = avg_daily_inc * days_remaining
    est_total_monthly_income = curr_income + est_future_income
    
    est_end_balance = est_total_monthly_income - est_total_monthly_expense
    est_savings = est_total_monthly_income - est_total_monthly_expense
    est_savings_rate = (est_savings / est_total_monthly_income * 100) if est_total_monthly_income > 0 else 0.0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card balance">
                <div class="metric-header">
                    <span class="metric-title">Proyeksi Saldo Akhir Bulan</span>
                    <div class="metric-icon-bg blue">🔮</div>
                </div>
                <div class="metric-value">{format_currency(est_end_balance)}</div>
                <div class="metric-subtitle">Estimasi saldo di tanggal {days_in_month}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            f"""
            <div class="metric-card expense">
                <div class="metric-header">
                    <span class="metric-title">Estimasi Total Pengeluaran</span>
                    <div class="metric-icon-bg red">📉</div>
                </div>
                <div class="metric-value">{format_currency(est_total_monthly_expense)}</div>
                <div class="metric-subtitle">Termasuk sisa {days_remaining} hari</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col3:
        st.markdown(
            f"""
            <div class="metric-card income">
                <div class="metric-header">
                    <span class="metric-title">Estimasi Tabungan Bersih</span>
                    <div class="metric-icon-bg green">💰</div>
                </div>
                <div class="metric-value">{format_currency(est_savings)}</div>
                <div class="metric-subtitle">Tingkat Tabungan: {format_percent(est_savings_rate, show_sign=False)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.info(
        f"💡 **Catatan Metode Proyeksi:** Perhitungan di atas berasumsi Anda mempertahankan laju pengeluaran rata-rata **{format_currency(avg_daily_exp)}/hari** untuk sisa **{days_remaining} hari** di bulan ini."
    )
