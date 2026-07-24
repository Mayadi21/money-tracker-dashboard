"""
Expense Category Distribution Donut Chart Component
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.constants import CATEGORY_COLORS, TYPE_EXPENSE
from utils.formatter import format_currency

def render_category_donut_chart(df: pd.DataFrame):
    """Render Donut Chart answering 'Where is my money going?'."""
    st.markdown('<div class="fin-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin-bottom: 0.25rem;">🍩 Distribusi Pengeluaran</h3>', unsafe_allow_html=True)
    st.caption("Menjawab: Ke mana saja uang saya keluar?")
    
    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    if expense_df.empty:
        st.info("Tidak ada data pengeluaran pada periode ini.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
        
    grouped = expense_df.groupby("Kategori")["Jumlah"].sum().reset_index()
    total_exp = grouped["Jumlah"].sum()
    
    fig = px.pie(
        grouped,
        names="Kategori",
        values="Jumlah",
        hole=0.6,
        color="Kategori",
        color_discrete_map=CATEGORY_COLORS
    )
    
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Nominal: Rp %{value:,.0f}<br>Proporsi: %{percent:.1%}<extra></extra>"
    )
    
    fig.update_layout(
        font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#334155"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        annotations=[
            dict(
                text=f"Total<br><b>{format_currency(total_exp, compact=True)}</b>",
                x=0.5, y=0.5,
                font_size=14,
                showarrow=False,
                font_family="Plus Jakarta Sans"
            )
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
