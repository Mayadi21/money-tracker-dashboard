"""
Cached time series aggregation functions with cumulative running totals (cumsum)
"""
import pandas as pd
import numpy as np
import streamlit as st
from utils.constants import TYPE_INCOME, TYPE_EXPENSE

@st.cache_data
def aggregate_daily(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate income and expense by calendar date and compute cumulative running totals."""
    if df.empty:
        return pd.DataFrame(columns=["PeriodKey", "PeriodLabel", TYPE_INCOME, TYPE_EXPENSE])
        
    temp = df.copy()
    temp["PeriodKey"] = temp["Tanggal"].dt.strftime("%Y-%m-%d")
    temp["PeriodLabel"] = temp["Tanggal"].dt.strftime("%d %b")
    
    # 1. Groupby date & sum
    grouped = temp.groupby(["PeriodKey", "PeriodLabel", "Jenis"])["Jumlah"].sum().unstack(fill_value=0).reset_index()
    
    if TYPE_INCOME not in grouped.columns:
        grouped[TYPE_INCOME] = 0.0
    if TYPE_EXPENSE not in grouped.columns:
        grouped[TYPE_EXPENSE] = 0.0

    # 2. Sort chronologically
    grouped = grouped.sort_values("PeriodKey").reset_index(drop=True)
    
    # 3. Apply cumulative sum (running totals)
    grouped[TYPE_INCOME] = grouped[TYPE_INCOME].cumsum()
    grouped[TYPE_EXPENSE] = grouped[TYPE_EXPENSE].cumsum()

    return grouped

@st.cache_data
def aggregate_weekly(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate income and expense by week and compute cumulative running totals."""
    if df.empty:
        return pd.DataFrame(columns=["PeriodKey", "PeriodLabel", TYPE_INCOME, TYPE_EXPENSE])
        
    temp = df.copy()
    temp["PeriodKey"] = temp["Tanggal"].dt.strftime("%G-W%V")
    temp["PeriodLabel"] = temp["Tanggal"].dt.strftime("Minggu %V, %Y")
    
    # 1. Groupby week & sum
    grouped = temp.groupby(["PeriodKey", "PeriodLabel", "Jenis"])["Jumlah"].sum().unstack(fill_value=0).reset_index()
    
    if TYPE_INCOME not in grouped.columns:
        grouped[TYPE_INCOME] = 0.0
    if TYPE_EXPENSE not in grouped.columns:
        grouped[TYPE_EXPENSE] = 0.0

    # 2. Sort chronologically
    grouped = grouped.sort_values("PeriodKey").reset_index(drop=True)

    # 3. Apply cumulative sum (running totals)
    grouped[TYPE_INCOME] = grouped[TYPE_INCOME].cumsum()
    grouped[TYPE_EXPENSE] = grouped[TYPE_EXPENSE].cumsum()

    return grouped

@st.cache_data
def aggregate_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate income and expense by month and compute cumulative running totals."""
    if df.empty:
        return pd.DataFrame(columns=["PeriodKey", "PeriodLabel", TYPE_INCOME, TYPE_EXPENSE])
        
    temp = df.copy()
    temp["PeriodKey"] = temp["Tanggal"].dt.strftime("%Y-%m")
    temp["PeriodLabel"] = temp["Tanggal"].dt.strftime("%b %Y")
    
    # 1. Groupby month & sum
    grouped = temp.groupby(["PeriodKey", "PeriodLabel", "Jenis"])["Jumlah"].sum().unstack(fill_value=0).reset_index()
    
    if TYPE_INCOME not in grouped.columns:
        grouped[TYPE_INCOME] = 0.0
    if TYPE_EXPENSE not in grouped.columns:
        grouped[TYPE_EXPENSE] = 0.0

    # 2. Sort chronologically
    grouped = grouped.sort_values("PeriodKey").reset_index(drop=True)

    # 3. Apply cumulative sum (running totals)
    grouped[TYPE_INCOME] = grouped[TYPE_INCOME].cumsum()
    grouped[TYPE_EXPENSE] = grouped[TYPE_EXPENSE].cumsum()

    return grouped
