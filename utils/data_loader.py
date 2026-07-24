"""
Data loading and preprocessing utilities with caching, secrets management, and fallback options
"""
import os
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from utils.constants import DAYS_INDONESIAN, TYPE_INCOME, TYPE_EXPENSE

def get_csv_url() -> str:
    """
    Safely retrieve Google Sheet CSV export URL from Streamlit secrets or environment variables.
    Prevents hardcoding sensitive spreadsheet IDs in public Git repositories.
    """
    # 1. Check Streamlit secrets
    try:
        if "google_sheets" in st.secrets:
            if "csv_url" in st.secrets["google_sheets"]:
                return st.secrets["google_sheets"]["csv_url"]
            elif "sheet_id" in st.secrets["google_sheets"]:
                sid = st.secrets["google_sheets"]["sheet_id"]
                return f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv"
        elif "CSV_URL" in st.secrets:
            return st.secrets["CSV_URL"]
        elif "SHEET_ID" in st.secrets:
            sid = st.secrets["SHEET_ID"]
            return f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv"
    except Exception:
        pass

    # 2. Check Environment Variables
    env_url = os.getenv("GOOGLE_SHEET_CSV_URL")
    if env_url:
        return env_url
    env_id = os.getenv("GOOGLE_SHEET_ID")
    if env_id:
        return f"https://docs.google.com/spreadsheets/d/{env_id}/export?format=csv"

    # 3. Fallback placeholder
    return "https://docs.google.com/spreadsheets/d/PLACEHOLDER_SHEET_ID/export?format=csv"

@st.cache_data(ttl=300)
def load_data(csv_url: str = None) -> pd.DataFrame:
    """
    Load transaction dataset from Google Sheet CSV URL or generate realistic sample data as fallback.
    """
    if csv_url is None:
        csv_url = get_csv_url()
        
    try:
        df = pd.read_csv(csv_url)
        df = preprocess_data(df)
        if df.empty:
            df = generate_sample_data()
        return df
    except Exception as e:
        st.warning(f"⚠️ Unable to load Google Sheet ({e}). Using generated sample dataset for demonstration.")
        return generate_sample_data()

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess, validate, and extract date features from raw DataFrame."""
    required_cols = ["Tanggal", "Jenis", "Kategori", "Jumlah"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
            
    df = df.dropna(subset=["Jenis", "Jumlah"]).copy()
    
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], format="%d/%m/%Y %H:%M:%S", errors="coerce")
    if df["Tanggal"].isna().any():
        df["Tanggal"] = df["Tanggal"].fillna(pd.to_datetime(df["Tanggal"], errors="coerce"))
    
    df = df.dropna(subset=["Tanggal"]).copy()
    
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    
    df["Jenis"] = df["Jenis"].astype(str).str.strip()
    df["Kategori"] = df["Kategori"].astype(str).str.strip()
    df["Catatan"] = df.get("Catatan", "").fillna("").astype(str)
    
    df = df.sort_values("Tanggal", ascending=True).reset_index(drop=True)
    
    df["Year"] = df["Tanggal"].dt.year
    df["Month"] = df["Tanggal"].dt.month
    df["YearMonth"] = df["Tanggal"].dt.strftime("%Y-%m")
    df["DayOfWeek"] = df["Tanggal"].dt.dayofweek
    df["DayName"] = df["DayOfWeek"].map(DAYS_INDONESIAN)
    df["DateOnly"] = df["Tanggal"].dt.date
    
    return df

def generate_sample_data(num_records: int = 120) -> pd.DataFrame:
    """Generate realistic 6-month sample transactions for demo/testing."""
    np.random.seed(42)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    categories_expense = ["Makanan & Minuman", "Transportasi", "Belanja", "Hiburan", "Tagihan", "Kesehatan", "Lainnya"]
    categories_income = ["Gaji", "Freelance Project", "Investasi", "Lainnya"]
    
    records = []
    current_date = start_date
    
    while current_date <= end_date:
        if current_date.day in [1, 25]:
            records.append({
                "Tanggal": current_date.replace(hour=9, minute=0, second=0),
                "Jenis": TYPE_INCOME,
                "Kategori": "Gaji",
                "Jumlah": 12000000,
                "Catatan": "Gaji Bulanan",
                "Pesan Balasan": "Pemasukan tercatat"
            })
            
        if np.random.rand() < 0.08:
            records.append({
                "Tanggal": current_date.replace(hour=14, minute=30, second=0),
                "Jenis": TYPE_INCOME,
                "Kategori": "Freelance Project",
                "Jumlah": np.random.choice([1500000, 2500000, 4000000]),
                "Catatan": "Pembayaran Project Web",
                "Pesan Balasan": "Pemasukan tercatat"
            })
            
        num_exp = np.random.randint(1, 4)
        for _ in range(num_exp):
            cat = np.random.choice(categories_expense, p=[0.35, 0.20, 0.15, 0.10, 0.10, 0.05, 0.05])
            if cat == "Makanan & Minuman":
                amt = np.random.choice([25000, 45000, 75000, 120000, 150000])
            elif cat == "Transportasi":
                amt = np.random.choice([15000, 35000, 80000, 150000])
            elif cat == "Tagihan":
                amt = np.random.choice([250000, 500000, 850000, 1200000])
            elif cat == "Belanja":
                amt = np.random.choice([150000, 350000, 750000])
            else:
                amt = np.random.choice([50000, 100000, 200000])
                
            hr = np.random.randint(8, 21)
            mn = np.random.randint(0, 59)
            records.append({
                "Tanggal": current_date.replace(hour=hr, minute=mn, second=0),
                "Jenis": TYPE_EXPENSE,
                "Kategori": cat,
                "Jumlah": float(amt),
                "Catatan": f"Transaksi {cat}",
                "Pesan Balasan": "Catatan pengeluaran tersimpan"
            })
            
        current_date += timedelta(days=1)
        
    df = pd.DataFrame(records)
    return preprocess_data(df)
