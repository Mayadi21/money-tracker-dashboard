"""
Category Budget Tracking Component
"""
import streamlit as st
import pandas as pd
from typing import Dict
from utils.constants import DEFAULT_CATEGORY_BUDGETS, TYPE_EXPENSE
from utils.formatter import format_currency

def render_budget_section(df: pd.DataFrame):
    """Render budget tracking cards with custom progress bars and alerts."""
    st.subheader("🎯 Melacak Anggaran (Budget Tracking)")
    st.markdown("Pantau batas anggaran bulanan per kategori untuk mengontrol pengeluaran.")
    
    if df.empty:
        st.info("Tidak ada data untuk pelacakan anggaran.")
        return
        
    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    spent_by_cat = expense_df.groupby("Kategori")["Jumlah"].sum().to_dict()
    
    # Initialize session state budgets if not present
    if "user_budgets" not in st.session_state:
        st.session_state["user_budgets"] = DEFAULT_CATEGORY_BUDGETS.copy()
        
    # Budget targets expander editor
    with st.expander("⚙️ Atur Batas Anggaran Kategori"):
        cols = st.columns(2)
        idx = 0
        all_categories = sorted(list(set(list(DEFAULT_CATEGORY_BUDGETS.keys()) + list(spent_by_cat.keys()))))
        
        for cat in all_categories:
            current_target = st.session_state["user_budgets"].get(cat, 1000000)
            col_target = cols[idx % 2]
            new_val = col_target.number_input(
                f"Anggaran: {cat}",
                min_value=100000,
                value=int(current_target),
                step=250000,
                format="%d"
            )
            st.session_state["user_budgets"][cat] = new_val
            idx += 1

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render Budget Progress Cards
    budgets = st.session_state["user_budgets"]
    
    for cat in sorted(budgets.keys()):
        budget_target = float(budgets[cat])
        spent = float(spent_by_cat.get(cat, 0.0))
        remaining = budget_target - spent
        pct = (spent / budget_target * 100) if budget_target > 0 else 0.0
        
        if pct > 100:
            status_cls = "danger"
            badge_text = "OVER BUDGET (TERLAMPAUI)"
            badge_bg = "#FEE2E2"
            badge_color = "#991B1B"
        elif pct >= 80:
            status_cls = "warning"
            badge_text = "PERINGATAN (≥ 80%)"
            badge_bg = "#FEF3C7"
            badge_color = "#92400E"
        else:
            status_cls = "safe"
            badge_text = "AMAN"
            badge_bg = "#DCFCE7"
            badge_color = "#166534"
            
        pct_width = min(pct, 100.0)
        
        st.markdown(
            f"""
            <div class="budget-card">
                <div class="budget-header">
                    <div>
                        <span class="budget-category">{cat}</span>
                        <span style="margin-left: 8px; background: {badge_bg}; color: {badge_color}; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">
                            {badge_text}
                        </span>
                    </div>
                    <div class="budget-stats">
                        Terpakai: <b>{format_currency(spent)}</b> / Anggaran: <b>{format_currency(budget_target)}</b> ({pct:.1f}%)
                    </div>
                </div>
                <div class="progress-track">
                    <div class="progress-fill {status_cls}" style="width: {pct_width}%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 6px; font-size: 0.8rem; color: #64748B;">
                    <span>Sisa Anggaran: <b style="color: {'#EF4444' if remaining < 0 else '#10B981'};">{format_currency(remaining)}</b></span>
                    <span>{100 - pct:.1f}% Tersisa</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
