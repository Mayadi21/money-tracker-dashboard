"""
Dual Donut Charts Component: Income Distribution (Left) & Expense Distribution (Right)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.constants import CATEGORY_COLORS, TYPE_INCOME, TYPE_EXPENSE
from utils.formatter import format_currency

def render_dual_donut_charts(df: pd.DataFrame):
    """Render side-by-side Dual Donut charts for Income and Expense distributions."""
    col_income, col_expense = st.columns(2)
    
    # ---------------------------------------------------
    # LEFT: INCOME DISTRIBUTION
    # ---------------------------------------------------
    with col_income:
        st.markdown('<div class="fin-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-size: 1.1rem; font-weight: 800; color: #0F172A; margin-bottom: 0.2rem;">💰 Distribusi Pemasukan</h3>', unsafe_allow_html=True)
        st.caption("Dari mana saja sumber pemasukan Anda?")
        
        inc_df = df[df["Jenis"] == TYPE_INCOME]
        if inc_df.empty:
            st.info("Tidak ada data pemasukan pada periode ini.")
        else:
            grouped_inc = inc_df.groupby("Kategori")["Jumlah"].sum().reset_index()
            total_inc = grouped_inc["Jumlah"].sum()
            
            fig_inc = px.pie(
                grouped_inc,
                names="Kategori",
                values="Jumlah",
                hole=0.6,
                color="Kategori",
                color_discrete_map=CATEGORY_COLORS
            )
            
            fig_inc.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate="<b>%{label}</b><br>Pemasukan: Rp %{value:,.0f}<br>Proporsi: %{percent:.1%}<extra></extra>"
            )
            
            fig_inc.update_layout(
                font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#334155"),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=300,
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
                annotations=[
                    dict(
                        text=f"Pemasukan<br><b>{format_currency(total_inc, compact=True)}</b>",
                        x=0.5, y=0.5,
                        font_size=13,
                        showarrow=False,
                        font_family="Plus Jakarta Sans"
                    )
                ]
            )
            st.plotly_chart(fig_inc, use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------
    # RIGHT: EXPENSE DISTRIBUTION
    # ---------------------------------------------------
    with col_expense:
        st.markdown('<div class="fin-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-size: 1.1rem; font-weight: 800; color: #0F172A; margin-bottom: 0.2rem;">📉 Distribusi Pengeluaran</h3>', unsafe_allow_html=True)
        st.caption("Ke mana saja uang Anda keluar?")
        
        exp_df = df[df["Jenis"] == TYPE_EXPENSE]
        if exp_df.empty:
            st.info("Tidak ada data pengeluaran pada periode ini.")
        else:
            grouped_exp = exp_df.groupby("Kategori")["Jumlah"].sum().reset_index()
            total_exp = grouped_exp["Jumlah"].sum()
            
            fig_exp = px.pie(
                grouped_exp,
                names="Kategori",
                values="Jumlah",
                hole=0.6,
                color="Kategori",
                color_discrete_map=CATEGORY_COLORS
            )
            
            fig_exp.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate="<b>%{label}</b><br>Pengeluaran: Rp %{value:,.0f}<br>Proporsi: %{percent:.1%}<extra></extra>"
            )
            
            fig_exp.update_layout(
                font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#334155"),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=300,
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
                annotations=[
                    dict(
                        text=f"Pengeluaran<br><b>{format_currency(total_exp, compact=True)}</b>",
                        x=0.5, y=0.5,
                        font_size=13,
                        showarrow=False,
                        font_family="Plus Jakarta Sans"
                    )
                ]
            )
            st.plotly_chart(fig_exp, use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
