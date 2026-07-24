"""
Header Component with Toolbar and Refresh Data Action
"""
import streamlit as st
from utils.refresh import refresh_dashboard


def render_header(
    title: str = "💸 Dashboard Keuangan",
    subtitle: str = "Aplikasi Keuangan Pribadi - Evaluasi Pemasukan, Pengeluaran & Arus Kas"
):
    """Render top modern header bar with status badge, info banner, and refresh button."""
    col_header, col_action = st.columns([4, 1], gap="medium")

    with col_header:
        html = f"""
        <div class="fin-header">
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
            <div>
                <span class="fin-header-badge">
                    FINANCE PRO
                </span>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    st.info("ℹ️ Data transaksi tidak diperbarui secara real-time. Silakan klik tombol **🔄 Refresh Data** di atas untuk memuat transaksi terbaru.")
    
    with col_action:
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Refresh Data", key="btn_refresh_dashboard", use_container_width=True, type="primary"):
            refresh_dashboard()

    



