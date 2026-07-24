"""
Transaction History Table Component with Badges, Pagination, and CSV Export
"""
import streamlit as st
import pandas as pd
from utils.formatter import format_currency, format_date
from utils.helpers import convert_df_to_csv
from utils.constants import TYPE_INCOME, TYPE_EXPENSE

def render_transaction_table(df: pd.DataFrame):
    """Render interactive transaction history table with badges and download button."""
    st.subheader("📋 Riwayat Transaksi")
    
    if df.empty:
        st.info("Tidak ada transaksi yang cocok dengan filter Anda.")
        return
        
    sorted_df = df.sort_values("Tanggal", ascending=False).reset_index(drop=True)
    
    # Search and page size control
    col_search, col_export = st.columns([3, 1])
    
    with col_search:
        st.caption(f"Menampilkan **{len(sorted_df):,}** transaksi")
        
    with col_export:
        csv_bytes = convert_df_to_csv(sorted_df)
        st.download_button(
            label="📥 Download CSV",
            data=csv_bytes,
            file_name="riwayat_transaksi_keuangan.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    # Styled Display DataFrame
    display_df = sorted_df.copy()
    display_df["Tanggal_Formatted"] = display_df["Tanggal"].apply(lambda d: format_date(d, "%d/%m/%Y %H:%M"))
    display_df["Jumlah_Formatted"] = display_df["Jumlah"].apply(lambda v: format_currency(v))
    
    # Select clean columns
    cols_to_show = ["Tanggal_Formatted", "Jenis", "Kategori", "Jumlah_Formatted", "Catatan"]
    renamed_cols = {
        "Tanggal_Formatted": "Waktu Transaksi",
        "Jenis": "Tipe",
        "Kategori": "Kategori",
        "Jumlah_Formatted": "Nominal",
        "Catatan": "Catatan / Keterangan"
    }
    
    table_view = display_df[cols_to_show].rename(columns=renamed_cols)
    
    st.dataframe(
        table_view,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nominal": st.column_config.TextColumn(
                "Nominal",
                help="Jumlah transaksi dalam Rupiah"
            ),
            "Tipe": st.column_config.TextColumn(
                "Tipe",
                help="Pemasukan atau Pengeluaran"
            )
        }
    )
