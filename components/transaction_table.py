"""
Compact Recent Transaction Table Component
"""
import streamlit as st
import pandas as pd
from utils.formatter import format_currency, format_date
from utils.helpers import convert_df_to_csv

def render_transaction_table(df: pd.DataFrame):
    """Render compact transaction table at the bottom of the dashboard."""
    st.markdown('<div class="fin-card">', unsafe_allow_html=True)
    
    col_hdr, col_exp = st.columns([3, 1])
    with col_hdr:
        st.markdown('<h3 style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 0;">📋 Riwayat Transaksi Terbaru</h3>', unsafe_allow_html=True)
        st.caption(f"Total {len(df):,} transaksi ditemukan")
        
    with col_exp:
        if not df.empty:
            csv_bytes = convert_df_to_csv(df)
            st.download_button(
                label="📥 Export CSV",
                data=csv_bytes,
                file_name="riwayat_transaksi.csv",
                mime="text/csv",
                use_container_width=True
            )
            
    if df.empty:
        st.info("Tidak ada transaksi untuk ditampilkan.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
        
    sorted_df = df.sort_values("Tanggal", ascending=False).reset_index(drop=True)
    
    # Prepare display dataframe
    display_df = sorted_df.copy()
    display_df["Tanggal_Formatted"] = display_df["Tanggal"].apply(lambda d: format_date(d, "%d %b %Y %H:%M"))
    display_df["Jumlah_Formatted"] = display_df["Jumlah"].apply(lambda v: format_currency(v))
    
    cols = ["Tanggal_Formatted", "Jenis", "Kategori", "Jumlah_Formatted", "Catatan"]
    renamed = {
        "Tanggal_Formatted": "Waktu",
        "Jenis": "Tipe",
        "Kategori": "Kategori",
        "Jumlah_Formatted": "Nominal",
        "Catatan": "Keterangan"
    }
    
    st.dataframe(
        display_df[cols].rename(columns=renamed),
        use_container_width=True,
        hide_index=True,
        height=320
    )
    st.markdown('</div>', unsafe_allow_html=True)
