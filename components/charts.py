"""
Interactive Plotly visualisations component
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.constants import (
    COLOR_PRIMARY, COLOR_SUCCESS, COLOR_DANGER, COLOR_WARNING,
    CATEGORY_COLORS, TYPE_INCOME, TYPE_EXPENSE, DAYS_INDONESIAN
)

# Standard layout template for Plotly charts
PLOTLY_LAYOUT_TEMPLATE = dict(
    font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#334155"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=40, b=20),
    hoverlabel=dict(bgcolor="#0F172A", font_size=12, font_family="Plus Jakarta Sans")
)

def render_category_donut_chart(df: pd.DataFrame):
    """1. Donut Chart: Expense distribution by category."""
    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    if expense_df.empty:
        st.info("Tidak ada data pengeluaran.")
        return
        
    grouped = expense_df.groupby("Kategori")["Jumlah"].sum().reset_index()
    
    fig = px.pie(
        grouped,
        names="Kategori",
        values="Jumlah",
        hole=0.55,
        color="Kategori",
        color_discrete_map=CATEGORY_COLORS,
        title="<b>Distribusi Pengeluaran per Kategori</b>"
    )
    
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Total: Rp %{value:,.0f}<br>Persentase: %{percent:.1%}<extra></extra>"
    )
    fig.update_layout(**PLOTLY_LAYOUT_TEMPLATE)
    st.plotly_chart(fig, use_container_width=True)

def render_daily_trend_line_chart(df: pd.DataFrame):
    """2. Line Chart: Daily income and expense trends over time."""
    if df.empty:
        st.info("Tidak ada data transaksi.")
        return
        
    daily = df.groupby(["DateOnly", "Jenis"])["Jumlah"].sum().unstack(fill_value=0).reset_index()
    if TYPE_INCOME not in daily.columns:
        daily[TYPE_INCOME] = 0.0
    if TYPE_EXPENSE not in daily.columns:
        daily[TYPE_EXPENSE] = 0.0
        
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily["DateOnly"],
        y=daily[TYPE_INCOME],
        name="Pemasukan",
        mode="lines+markers",
        line=dict(color=COLOR_SUCCESS, width=3, shape="spline"),
        marker=dict(size=6),
        hovertemplate="Tanggal: %{x}<br>Pemasukan: Rp %{y:,.0f}<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=daily["DateOnly"],
        y=daily[TYPE_EXPENSE],
        name="Pengeluaran",
        mode="lines+markers",
        line=dict(color=COLOR_DANGER, width=3, shape="spline"),
        marker=dict(size=6),
        hovertemplate="Tanggal: %{x}<br>Pengeluaran: Rp %{y:,.0f}<extra></extra>"
    ))
    
    fig.update_layout(
        title="<b>Tren Harian Pemasukan & Pengeluaran</b>",
        xaxis_title="Tanggal",
        yaxis_title="Jumlah (Rp)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **PLOTLY_LAYOUT_TEMPLATE
    )
    st.plotly_chart(fig, use_container_width=True)

def render_cumulative_balance_area_chart(df: pd.DataFrame):
    """3. Area Chart: Cumulative net balance over time."""
    if df.empty:
        st.info("Tidak ada data transaksi.")
        return
        
    sorted_df = df.sort_values("Tanggal").copy()
    sorted_df["SignedAmount"] = np.where(
        sorted_df["Jenis"] == TYPE_INCOME,
        sorted_df["Jumlah"],
        -sorted_df["Jumlah"]
    )
    sorted_df["CumulativeBalance"] = sorted_df["SignedAmount"].cumsum()
    
    daily_cum = sorted_df.groupby("DateOnly")["CumulativeBalance"].last().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_cum["DateOnly"],
        y=daily_cum["CumulativeBalance"],
        name="Saldo Kumulatif",
        fill="tozeroy",
        fillcolor="rgba(37, 99, 235, 0.15)",
        line=dict(color=COLOR_PRIMARY, width=3),
        hovertemplate="Tanggal: %{x}<br>Saldo: Rp %{y:,.0f}<extra></extra>"
    ))
    
    fig.update_layout(
        title="<b>Pertumbuhan Akumulasi Saldo</b>",
        xaxis_title="Tanggal",
        yaxis_title="Saldo Kumulatif (Rp)",
        **PLOTLY_LAYOUT_TEMPLATE
    )
    st.plotly_chart(fig, use_container_width=True)

def render_monthly_cash_flow_chart(df: pd.DataFrame):
    """4. Monthly Cash Flow: Income vs Expenses bar chart."""
    if df.empty:
        st.info("Tidak ada data transaksi.")
        return
        
    monthly = df.groupby(["YearMonth", "Jenis"])["Jumlah"].sum().unstack(fill_value=0).reset_index()
    if TYPE_INCOME not in monthly.columns:
        monthly[TYPE_INCOME] = 0.0
    if TYPE_EXPENSE not in monthly.columns:
        monthly[TYPE_EXPENSE] = 0.0
        
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly["YearMonth"],
        y=monthly[TYPE_INCOME],
        name="Pemasukan",
        marker_color=COLOR_SUCCESS,
        hovertemplate="Bulan: %{x}<br>Pemasukan: Rp %{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=monthly["YearMonth"],
        y=monthly[TYPE_EXPENSE],
        name="Pengeluaran",
        marker_color=COLOR_DANGER,
        hovertemplate="Bulan: %{x}<br>Pengeluaran: Rp %{y:,.0f}<extra></extra>"
    ))
    
    fig.update_layout(
        barmode="group",
        title="<b>Arus Kas Bulanan (Pemasukan vs Pengeluaran)</b>",
        xaxis_title="Bulan",
        yaxis_title="Total (Rp)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **PLOTLY_LAYOUT_TEMPLATE
    )
    st.plotly_chart(fig, use_container_width=True)

def render_top_expense_categories_bar(df: pd.DataFrame):
    """5. Bar Chart: Top 10 expense categories."""
    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    if expense_df.empty:
        st.info("Tidak ada data pengeluaran.")
        return
        
    top_cat = expense_df.groupby("Kategori")["Jumlah"].sum().reset_index()
    top_cat = top_cat.sort_values("Jumlah", ascending=True).tail(10)
    
    fig = px.bar(
        top_cat,
        x="Jumlah",
        y="Kategori",
        orientation="h",
        text_auto=".2s",
        color="Jumlah",
        color_continuous_scale="Reds",
        title="<b>Top 10 Kategori Pengeluaran Terbesar</b>"
    )
    
    fig.update_traces(
        hovertemplate="Kategori: %{y}<br>Total: Rp %{x:,.0f}<extra></extra>"
    )
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Total Pengeluaran (Rp)",
        yaxis_title="Kategori",
        **PLOTLY_LAYOUT_TEMPLATE
    )
    st.plotly_chart(fig, use_container_width=True)

def render_expense_treemap(df: pd.DataFrame):
    """6. Treemap: Expense distribution visualization."""
    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    if expense_df.empty:
        st.info("Tidak ada data pengeluaran.")
        return
        
    grouped = expense_df.groupby(["Kategori"])["Jumlah"].sum().reset_index()
    
    fig = px.treemap(
        grouped,
        path=["Kategori"],
        values="Jumlah",
        color="Jumlah",
        color_continuous_scale="Blues",
        title="<b>Treemap Proporsi Pengeluaran</b>"
    )
    
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Total: Rp %{value:,.0f}<extra></extra>"
    )
    fig.update_layout(**PLOTLY_LAYOUT_TEMPLATE)
    st.plotly_chart(fig, use_container_width=True)

def render_transaction_scatter_plot(df: pd.DataFrame):
    """7. Scatter Plot: Transaction amounts over time colored by category."""
    if df.empty:
        st.info("Tidak ada data transaksi.")
        return
        
    fig = px.scatter(
        df,
        x="Tanggal",
        y="Jumlah",
        color="Kategori",
        symbol="Jenis",
        size="Jumlah",
        size_max=25,
        hover_data=["Catatan", "Jenis"],
        title="<b>Sebaran Transaksi Keuangan</b>"
    )
    
    fig.update_traces(
        hovertemplate="Tanggal: %{x}<br>Jumlah: Rp %{y:,.0f}<br>Kategori: %{customdata[0]}<extra></extra>"
    )
    fig.update_layout(
        yaxis_title="Nominal (Rp)",
        xaxis_title="Waktu",
        **PLOTLY_LAYOUT_TEMPLATE
    )
    st.plotly_chart(fig, use_container_width=True)

def render_calendar_heatmap(df: pd.DataFrame):
    """8. Calendar Heatmap: Daily transaction intensity heatmap."""
    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    if expense_df.empty:
        st.info("Tidak ada data pengeluaran.")
        return
        
    daily = expense_df.groupby("DateOnly")["Jumlah"].sum().reset_index()
    daily["Date"] = pd.to_datetime(daily["DateOnly"])
    daily["Week"] = daily["Date"].dt.isocalendar().week
    daily["DayOfWeek"] = daily["Date"].dt.dayofweek
    
    # Pivot table for heatmap matrix
    heatmap_data = daily.pivot_table(index="DayOfWeek", columns="Week", values="Jumlah", aggfunc="sum").fillna(0)
    
    day_labels = [DAYS_INDONESIAN[i] for i in range(7)]
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=[f"W{w}" for w in heatmap_data.columns],
        y=day_labels,
        colorscale="YlOrRd",
        hovertemplate="Hari: %{y}<br>Minggu ke: %{x}<br>Total Pengeluaran: Rp %{z:,.0f}<extra></extra>"
    ))
    
    fig.update_layout(
        title="<b>Heatmap Intensitas Pengeluaran Harian</b>",
        xaxis_title="Minggu dalam Tahun",
        yaxis_title="Hari dalam Minggu",
        **PLOTLY_LAYOUT_TEMPLATE
    )
    st.plotly_chart(fig, use_container_width=True)

def render_weekly_spending_trend(df: pd.DataFrame):
    """9. Weekly Spending Trend: Total expenses breakdown by day of week."""
    expense_df = df[df["Jenis"] == TYPE_EXPENSE]
    if expense_df.empty:
        st.info("Tidak ada data pengeluaran.")
        return
        
    weekly = expense_df.groupby(["DayOfWeek", "DayName"])["Jumlah"].sum().reset_index()
    weekly = weekly.sort_values("DayOfWeek")
    
    fig = px.bar(
        weekly,
        x="DayName",
        y="Jumlah",
        color="Jumlah",
        color_continuous_scale="Purples",
        title="<b>Pola Pengeluaran Berdasarkan Hari</b>"
    )
    
    fig.update_traces(
        hovertemplate="Hari: %{x}<br>Total Pengeluaran: Rp %{y:,.0f}<extra></extra>"
    )
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Hari dalam Seminggu",
        yaxis_title="Total Pengeluaran (Rp)",
        **PLOTLY_LAYOUT_TEMPLATE
    )
    st.plotly_chart(fig, use_container_width=True)

def render_monthly_financial_trend(df: pd.DataFrame):
    """10. Monthly Financial Trend: Combo bar chart + net balance overlay line."""
    if df.empty:
        st.info("Tidak ada data transaksi.")
        return
        
    monthly = df.groupby(["YearMonth", "Jenis"])["Jumlah"].sum().unstack(fill_value=0).reset_index()
    if TYPE_INCOME not in monthly.columns:
        monthly[TYPE_INCOME] = 0.0
    if TYPE_EXPENSE not in monthly.columns:
        monthly[TYPE_EXPENSE] = 0.0
        
    monthly["NetBalance"] = monthly[TYPE_INCOME] - monthly[TYPE_EXPENSE]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=monthly["YearMonth"],
        y=monthly[TYPE_INCOME],
        name="Pemasukan",
        marker_color=COLOR_SUCCESS
    ))
    
    fig.add_trace(go.Bar(
        x=monthly["YearMonth"],
        y=monthly[TYPE_EXPENSE],
        name="Pengeluaran",
        marker_color=COLOR_DANGER
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly["YearMonth"],
        y=monthly["NetBalance"],
        name="Net Saldo",
        mode="lines+markers",
        line=dict(color=COLOR_PRIMARY, width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="<b>Evaluasi Tren Keuangan Bulanan</b>",
        barmode="group",
        xaxis_title="Bulan",
        yaxis_title="Total (Rp)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **PLOTLY_LAYOUT_TEMPLATE
    )
    st.plotly_chart(fig, use_container_width=True)
