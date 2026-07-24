"""
Hero Section: Cumulative Cash Flow Running Totals Line Chart
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.aggregation import aggregate_daily, aggregate_weekly, aggregate_monthly
from utils.constants import COLOR_SUCCESS, COLOR_DANGER, TYPE_INCOME, TYPE_EXPENSE

def render_cashflow_hero_chart(df: pd.DataFrame):
    """
    Render full-width hero Cumulative Cash Flow line chart (running totals).
    Time aggregation level is controlled via Daily | Weekly | Monthly selector.
    """
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    
    col_title, col_toggle = st.columns([2, 1])
    
    with col_title:
        st.markdown('<h3 class="hero-title">📈 Kumulatif Pemasukan vs Pengeluaran</h3>', unsafe_allow_html=True)
        st.caption("Grafik akumulasi arus kas kumulatif (Running Totals)")
        
    with col_toggle:
        # Aggregation level toggle (Daily | Weekly | Monthly)
        granularity = st.radio(
            "Agregasi Waktu",
            options=["Daily", "Weekly", "Monthly"],
            horizontal=True,
            index=0,
            key="cashflow_granularity_toggle",
            label_visibility="collapsed"
        )

    if df.empty:
        st.info("Tidak ada data transaksi pada rentang waktu ini.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Call cached cumulative aggregation functions
    if granularity == "Daily":
        agg_df = aggregate_daily(df)
    elif granularity == "Weekly":
        agg_df = aggregate_weekly(df)
    else:
        agg_df = aggregate_monthly(df)

    if agg_df.empty:
        st.info("Tidak ada data teragregasi.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Plotly Hero Line Chart (Cumulative Running Totals)
    fig = go.Figure()

    # Cumulative Income Line (Green - Always non-decreasing)
    fig.add_trace(go.Scatter(
        x=agg_df["PeriodLabel"],
        y=agg_df[TYPE_INCOME],
        name="Akumulasi Pemasukan",
        mode="lines+markers",
        line=dict(color=COLOR_SUCCESS, width=3.5, shape="spline"),
        marker=dict(size=7, color=COLOR_SUCCESS),
        hovertemplate="Periode: %{x}<br>Kumulatif Pemasukan: Rp %{y:,.0f}<extra></extra>"
    ))

    # Cumulative Expense Line (Red - Always non-decreasing)
    fig.add_trace(go.Scatter(
        x=agg_df["PeriodLabel"],
        y=agg_df[TYPE_EXPENSE],
        name="Akumulasi Pengeluaran",
        mode="lines+markers",
        line=dict(color=COLOR_DANGER, width=3.5, shape="spline"),
        marker=dict(size=7, color=COLOR_DANGER),
        hovertemplate="Periode: %{x}<br>Kumulatif Pengeluaran: Rp %{y:,.0f}<extra></extra>"
    ))

    fig.update_layout(
        font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#334155"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin=dict(l=10, r=10, t=20, b=10),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12, weight="bold")
        ),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
