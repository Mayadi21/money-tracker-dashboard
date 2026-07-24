"""
Header Component
"""
import streamlit as st

def render_header(title: str = "💸 Money Tracker Dashboard", subtitle: str = "Ringkasan Kesehatan Keuangan & Pengambilan Keputusan"):
    """Render top modern header bar."""
    html = f"""
    <div class="fin-header">
        <div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 700;">
                FINANCE PRO
            </span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
