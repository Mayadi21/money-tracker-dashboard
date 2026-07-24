"""
Smart Financial Alerts Component
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any
from utils.formatter import format_currency, format_percent
from utils.constants import TYPE_EXPENSE, TYPE_INCOME

def render_smart_alerts(kpis: Dict[str, Any], df: pd.DataFrame):
    """Evaluate and render smart alert cards based on financial conditions."""
    if df.empty:
        return
        
    alerts = []
    
    total_inc = kpis["total_income"]
    total_exp = kpis["total_expense"]
    savings_rate = kpis["savings_rate"]
    
    # 1. Expenses exceed income
    if total_exp > total_inc and total_inc > 0:
        alerts.append({
            "type": "danger",
            "title": "🚨 Defisit Keuangan Detected",
            "desc": f"Pengeluaran Anda ({format_currency(total_exp)}) melebihi pemasukan ({format_currency(total_inc)}). Pertimbangkan untuk mengerem pengeluaran sekunder."
        })
        
    # 2. Savings rate below 20%
    if total_inc > 0 and savings_rate < 20.0 and savings_rate >= 0:
        alerts.append({
            "type": "warning",
            "title": "⚠️ Savings Rate Rendah (< 20%)",
            "desc": f"Tingkat tabungan Anda saat ini adalah {format_percent(savings_rate, show_sign=False)}. Rekomendasi keuangan ideal adalah menyisihkan minimal 20% dari pemasukan."
        })
        
    # 3. Zero income recorded
    if total_inc == 0 and total_exp > 0:
        alerts.append({
            "type": "warning",
            "title": "⚠️ Tidak Ada Pemasukan Tercatat",
            "desc": "Tidak ditemukan pencatatan pemasukan pada periode yang dipilih."
        })
        
    # 4. Single category expense > 40%
    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    if not expense_df.empty and total_exp > 0:
        cat_sums = expense_df.groupby("Kategori")["Jumlah"].sum()
        for cat, amt in cat_sums.items():
            pct = (amt / total_exp) * 100
            if pct >= 40.0:
                alerts.append({
                    "type": "warning",
                    "title": f"🔔 Konsentrasi Pengeluaran: {cat} ({pct:.1f}%)",
                    "desc": f"Kategori <b>{cat}</b> menyerap <b>{pct:.1f}%</b> dari total pengeluaran ({format_currency(amt)}). Waspadai dominasi biaya pada satu kategori ini."
                })
                
    # Render Alerts if any exist
    if alerts:
        st.markdown('<div style="margin-bottom: 1rem;">', unsafe_allow_html=True)
        for alert in alerts:
            css_cls = f"fin-alert-{alert['type']}"
            st.markdown(
                f"""
                <div class="fin-alert {css_cls}">
                    <div>
                        <div class="fin-alert-title">{alert['title']}</div>
                        <div class="fin-alert-desc">{alert['desc']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
