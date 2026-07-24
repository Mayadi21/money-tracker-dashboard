"""
Comprehensive statistical and financial analysis functions
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple
from utils.constants import TYPE_INCOME, TYPE_EXPENSE, DAYS_INDONESIAN

def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate summary financial KPI metrics from transaction dataframe."""
    if df.empty:
        return {
            "total_income": 0.0,
            "total_expense": 0.0,
            "net_balance": 0.0,
            "savings_rate": 0.0,
            "total_transactions": 0,
            "num_categories": 0,
            "active_days": 0,
            "avg_daily_expense": 0.0,
            "avg_daily_income": 0.0,
            "monthly_cash_flow": 0.0
        }
        
    income_df = df[df["Jenis"] == TYPE_INCOME]
    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    
    total_income = float(income_df["Jumlah"].sum())
    total_expense = float(expense_df["Jumlah"].sum())
    net_balance = total_income - total_expense
    
    savings_rate = ((total_income - total_expense) / total_income * 100) if total_income > 0 else 0.0
    
    # Active days
    unique_dates = df["DateOnly"].nunique()
    active_days = max(unique_dates, 1)
    
    avg_daily_expense = total_expense / active_days
    avg_daily_income = total_income / active_days
    
    num_categories = df["Kategori"].nunique()
    total_transactions = len(df)
    monthly_cash_flow = net_balance
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance,
        "savings_rate": savings_rate,
        "total_transactions": total_transactions,
        "num_categories": num_categories,
        "active_days": active_days,
        "avg_daily_expense": avg_daily_expense,
        "avg_daily_income": avg_daily_income,
        "monthly_cash_flow": monthly_cash_flow
    }

def calculate_period_deltas(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate percentage changes comparing the recent half of the date range to the prior half.
    """
    if df.empty or df["DateOnly"].nunique() < 2:
        return {"income_delta": 0.0, "expense_delta": 0.0, "balance_delta": 0.0}
        
    min_date = df["DateOnly"].min()
    max_date = df["DateOnly"].max()
    mid_date = min_date + (max_date - min_date) / 2
    
    curr_df = df[df["DateOnly"] > mid_date]
    prev_df = df[df["DateOnly"] <= mid_date]
    
    curr_inc = curr_df[curr_df["Jenis"] == TYPE_INCOME]["Jumlah"].sum()
    prev_inc = prev_df[prev_df["Jenis"] == TYPE_INCOME]["Jumlah"].sum()
    
    curr_exp = curr_df[curr_df["Jenis"] == TYPE_EXPENSE]["Jumlah"].sum()
    prev_exp = prev_df[prev_df["Jenis"] == TYPE_EXPENSE]["Jumlah"].sum()
    
    inc_delta = ((curr_inc - prev_inc) / prev_inc * 100) if prev_inc > 0 else 0.0
    exp_delta = ((curr_exp - prev_exp) / prev_exp * 100) if prev_exp > 0 else 0.0
    
    return {
        "income_delta": inc_delta,
        "expense_delta": exp_delta,
        "balance_delta": (curr_inc - curr_exp) - (prev_inc - prev_exp)
    }

def get_transaction_extremes(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate min, max, and average transaction metrics."""
    if df.empty:
        return {
            "largest_tx": 0, "smallest_tx": 0, "avg_tx": 0,
            "avg_income_tx": 0, "avg_expense_tx": 0
        }
        
    income_df = df[df["Jenis"] == TYPE_INCOME]
    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    
    return {
        "largest_tx": float(df["Jumlah"].max()) if not df.empty else 0,
        "smallest_tx": float(df["Jumlah"].min()) if not df.empty else 0,
        "avg_tx": float(df["Jumlah"].mean()) if not df.empty else 0,
        "avg_income_tx": float(income_df["Jumlah"].mean()) if not income_df.empty else 0,
        "avg_expense_tx": float(expense_df["Jumlah"].mean()) if not expense_df.empty else 0,
    }

def analyze_spending_behavior(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze category and day-of-week spending patterns and streak lengths."""
    empty_res = {
        "most_expensive_category": ("N/A", 0),
        "least_expensive_category": ("N/A", 0),
        "most_active_category": ("N/A", 0),
        "most_expensive_day": ("N/A", 0),
        "most_active_day": ("N/A", 0),
        "streak_without_expenses": 0,
        "streak_with_expenses": 0
    }
    if df.empty:
        return empty_res
        
    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    if expense_df.empty:
        return empty_res
        
    # Category spending
    cat_grouped = expense_df.groupby("Kategori")["Jumlah"].agg(["sum", "count"])
    most_exp_cat = (cat_grouped["sum"].idxmax(), cat_grouped["sum"].max())
    least_exp_cat = (cat_grouped["sum"].idxmin(), cat_grouped["sum"].min())
    most_act_cat = (cat_grouped["count"].idxmax(), cat_grouped["count"].max())
    
    # Day of week analysis
    day_grouped = expense_df.groupby("DayName")["Jumlah"].agg(["sum", "count"])
    most_exp_day = (day_grouped["sum"].idxmax(), day_grouped["sum"].max())
    most_act_day = (day_grouped["count"].idxmax(), day_grouped["count"].max())
    
    # Streaks calculation
    all_dates = pd.date_range(start=df["DateOnly"].min(), end=df["DateOnly"].max()).date
    expense_dates = set(expense_df["DateOnly"].unique())
    
    current_no_exp_streak = 0
    max_no_exp_streak = 0
    current_exp_streak = 0
    max_exp_streak = 0
    
    for d in all_dates:
        if d in expense_dates:
            current_exp_streak += 1
            max_exp_streak = max(max_exp_streak, current_exp_streak)
            current_no_exp_streak = 0
        else:
            current_no_exp_streak += 1
            max_no_exp_streak = max(max_no_exp_streak, current_no_exp_streak)
            current_exp_streak = 0
            
    return {
        "most_expensive_category": most_exp_cat,
        "least_expensive_category": least_exp_cat,
        "most_active_category": most_act_cat,
        "most_expensive_day": most_exp_day,
        "most_active_day": most_act_day,
        "streak_without_expenses": max_no_exp_streak,
        "streak_with_expenses": max_exp_streak
    }

def compute_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compute monthly breakdown with growth rates and trend indicators."""
    if df.empty:
        return pd.DataFrame(columns=["YearMonth", "Pemasukan", "Pengeluaran", "Saldo", "SavingsRate", "Growth%"])
        
    monthly = df.groupby(["YearMonth", "Jenis"])["Jumlah"].sum().unstack(fill_value=0).reset_index()
    
    if TYPE_INCOME not in monthly.columns:
        monthly[TYPE_INCOME] = 0.0
    if TYPE_EXPENSE not in monthly.columns:
        monthly[TYPE_EXPENSE] = 0.0
        
    monthly["Saldo"] = monthly[TYPE_INCOME] - monthly[TYPE_EXPENSE]
    monthly["SavingsRate"] = np.where(
        monthly[TYPE_INCOME] > 0,
        (monthly["Saldo"] / monthly[TYPE_INCOME]) * 100,
        0.0
    )
    
    # Growth calculation vs previous month
    monthly["PrevExpense"] = monthly[TYPE_EXPENSE].shift(1)
    monthly["Growth%"] = np.where(
        monthly["PrevExpense"] > 0,
        ((monthly[TYPE_EXPENSE] - monthly["PrevExpense"]) / monthly["PrevExpense"]) * 100,
        0.0
    )
    
    return monthly
