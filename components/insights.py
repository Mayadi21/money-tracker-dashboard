"""
Top 3 Scannable Financial Insights Component
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any
from utils.formatter import format_currency, format_percent
from utils.constants import TYPE_EXPENSE

def render_top_3_insights(kpis: Dict[str, Any], behavior: Dict[str, Any], deltas: Dict[str, float], df: pd.DataFrame):
    """Render strictly the 3 most important scannable financial insights."""
    st.markdown('<div class="fin-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin-bottom: 1rem;">💡 Top 3 Insight Penting</h3>', unsafe_allow_html=True)
    
    if df.empty:
        st.info("Belum ada data untuk menghasilkan insight.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    total_exp = kpis["total_expense"]
    
    # 1. Insight 1: Largest Spending Category
    top_cat, top_amt = behavior.get("most_expensive_category", ("N/A", 0))
    cat_pct = (top_amt / total_exp * 100) if total_exp > 0 else 0.0
    insight1_title = f"🏷️ Kategori Terbesar: {top_cat}"
    insight1_desc = f"Menyerap <b>{cat_pct:.1f}%</b> dari total pengeluaran ({format_currency(top_amt)})."
    
    # 2. Insight 2: Spending Growth Trend
    exp_delta = deltas.get("expense_delta", 0)
    if exp_delta > 0:
        insight2_title = "📈 Pengeluaran Meningkat"
        insight2_desc = f"Pengeluaran naik <b>+{exp_delta:.1f}%</b> dibandingkan periode sebelumnya."
    elif exp_delta < 0:
        insight2_title = "📉 Pengeluaran Hemat"
        insight2_desc = f"Pengeluaran berhasil ditekan <b>{exp_delta:.1f}%</b> dari periode sebelumnya."
    else:
        insight2_title = "▬ Pengeluaran Stabil"
        insight2_desc = "Volume pengeluaran relatif sama dengan periode sebelumnya."

    # 3. Insight 3: Savings Rate Status
    sr = kpis["savings_rate"]
    if sr >= 20.0:
        insight3_title = "✅ Savings Rate Sehat"
        insight3_desc = f"Tingkat tabungan Anda <b>{format_percent(sr, show_sign=False)}</b> (Mencapai target ideal ≥ 20%)."
    elif sr > 0:
        insight3_title = "⚠️ Savings Rate Perlu Ditingkatkan"
        insight3_desc = f"Tingkat tabungan <b>{format_percent(sr, show_sign=False)}</b> berada di bawah target ideal 20%."
    else:
        insight3_title = "🚨 Perhatian Arus Kas Defisit"
        insight3_desc = "Pengeluaran melebihi pemasukan pada periode ini."

    # Render 3 Insight Cards
    _render_insight_card(insight1_title, insight1_desc, "#2563EB")
    _render_insight_card(insight2_title, insight2_desc, "#F59E0B" if exp_delta > 0 else "#10B981")
    _render_insight_card(insight3_title, insight3_desc, "#10B981" if sr >= 20 else "#EF4444")
    
    st.markdown('</div>', unsafe_allow_html=True)

def _render_insight_card(title: str, desc: str, border_color: str):
    """HTML helper for insight card."""
    html = f"""
    <div class="insight-card" style="border-left-color: {border_color};">
        <div class="insight-card-title">{title}</div>
        <div class="insight-card-desc">{desc}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
