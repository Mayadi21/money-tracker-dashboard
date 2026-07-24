"""
Primary KPI Cards Component: Total Income, Total Expense, Net Cash Flow
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any
from utils.formatter import format_currency
from utils.constants import TYPE_INCOME, TYPE_EXPENSE

def render_primary_kpi_cards(df: pd.DataFrame):
    """
    Render 3 clean, prominent KPI cards:
    1. Total Income (with Income Transactions count in subtext)
    2. Total Expense (with Expense Transactions count in subtext)
    3. Net Cash Flow (Total Income - Total Expense)
    """
    income_df = df[df["Jenis"] == TYPE_INCOME]
    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    
    total_income = income_df["Jumlah"].sum() if not income_df.empty else 0.0
    total_expense = expense_df["Jumlah"].sum() if not expense_df.empty else 0.0
    net_cashflow = total_income - total_expense
    
    expense_tx_count = len(expense_df)
    income_tx_count = len(income_df)
    
    c1, c2, c3 = st.columns(3)
    
    # 1. Total Income Card
    with c1:
        _render_card(
            title="Total Income",
            value=format_currency(total_income),
            icon="💰",
            theme="income",
            subtext=f"📊 {income_tx_count} Transaksi Pemasukan"
        )
        
    # 2. Total Expense Card
    with c2:
        _render_card(
            title="Total Expense",
            value=format_currency(total_expense),
            icon="📉",
            theme="expense",
            subtext=f"📊 {expense_tx_count} Transaksi Pengeluaran"
        )
        
    # 3. Net Cash Flow Card
    with c3:
        net_theme = "income" if net_cashflow >= 0 else "expense"
        net_icon = "⚖️" if net_cashflow >= 0 else "🚨"
        sign = "+" if net_cashflow > 0 else ""
        _render_card(
            title="Net Cash Flow",
            value=f"{sign}{format_currency(net_cashflow)}",
            icon=net_icon,
            theme=net_theme,
            subtext="Arus Kas Bersih (Pemasukan - Pengeluaran)"
        )

def _render_card(title: str, value: str, icon: str, theme: str, subtext: str = ""):
    """Render single clean KPI card HTML."""
    html = f"""
    <div class="kpi-card {theme}">
        <div class="kpi-header">
            <span class="kpi-title">{title}</span>
            <span class="kpi-icon">{icon}</span>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">
            <span>{subtext}</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
