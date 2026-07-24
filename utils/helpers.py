"""
UI helper functions for Streamlit rendering and CSS injection
"""
import streamlit as st
import os
import pandas as pd

def load_css(css_path: str = "assets/styles.css"):
    """Inject custom CSS stylesheet into Streamlit app."""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found at {css_path}")

def render_header(title: str = "💸 Money Tracker Dashboard", subtitle: str = "Modern Personal Finance Management & Insights"):
    """Render fintech dashboard header card."""
    html = f"""
    <div class="fin-header">
        <div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                PRO DASHBOARD
            </span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_empty_state(message: str = "No transactions found matching your selected filters."):
    """Render friendly empty state component."""
    st.info(f"🔍 {message}")

def convert_df_to_csv(df: pd.DataFrame) -> bytes:
    """Convert dataframe to CSV byte stream for downloading."""
    return df.to_csv(index=False).encode('utf-8')
