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
    Safely retrieve Google Sheet CSV export URL exclusively from Streamlit secrets or environment variables.
    Returns None if no secret or environment variable is configured.
    """
    # 1. Check Streamlit secrets
    try:
        if "google_sheets" in st.secrets:
            url = st.secrets["google_sheets"].get("csv_url", "")
            sid = st.secrets["google_sheets"].get("sheet_id", "")
            if url and "YOUR_GOOGLE_SHEET" not in url and "PLACEHOLDER" not in url:
                return url
            elif sid and "YOUR_GOOGLE_SHEET" not in sid and "PLACEHOLDER" not in sid:
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

    return None

@st.cache_data(ttl=300)
def load_data(csv_url: str = None) -> pd.DataFrame:
    """
    Load transaction dataset from Google Sheet CSV URL or generate sample data as fallback.
    """
    if csv_url is None:
        csv_url = get_csv_url()
        
    if not csv_url:
        return generate_sample_data()

    try:
        df = pd.read_csv(csv_url)
        df = preprocess_data(df)
        if df.empty:
            df = generate_sample_data()
        return df
    except Exception:
        return generate_sample_data()

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess, validate, and extract date features directly from raw CSV."""
    if df.empty:
        return df
        
    # Clean column headers (strip whitespace and extra quotes)
    df.columns = df.columns.astype(str).str.strip().str.replace("'", "").str.replace('"', '')
    
    # Map flexible/alternative column names directly to standard columns
    col_map = {}
    for col in df.columns:
        c_lower = col.lower().strip()
        if c_lower in ["catatan", "keterangan", "note", "notes", "description"]:
            col_map[col] = "Catatan"
        elif c_lower in ["tanggal", "date", "time", "waktu"]:
            col_map[col] = "Tanggal"
        elif c_lower in ["jenis", "type", "tipe"]:
            col_map[col] = "Jenis"
        elif c_lower in ["kategori", "category"]:
            col_map[col] = "Kategori"
        elif c_lower in ["jumlah", "amount", "nominal"]:
            col_map[col] = "Jumlah"
            
    if col_map:
        df = df.rename(columns=col_map)

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
    
    if "Catatan" in df.columns:
        df["Catatan"] = df["Catatan"].fillna("").astype(str).str.strip()
    else:
        df["Catatan"] = ""
    
    df = df.sort_values("Tanggal", ascending=True).reset_index(drop=True)
    
    df["Year"] = df["Tanggal"].dt.year
    df["Month"] = df["Tanggal"].dt.month
    df["YearMonth"] = df["Tanggal"].dt.strftime("%Y-%m")
    df["DayOfWeek"] = df["Tanggal"].dt.dayofweek
    df["DayName"] = df["DayOfWeek"].map(DAYS_INDONESIAN)
    df["DateOnly"] = df["Tanggal"].dt.date
    
    return df

def generate_sample_data(num_records: int = 120) -> pd.DataFrame:
    """Generate sample transactions for offline demo fallback."""
    np.random.seed(42)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    categories_expense = ["Makanan & Minuman", "Transportasi", "Belanja", "Hiburan", "Tagihan", "Kesehatan", "Lainnya"]
    
    sample_notes = {
        "Makanan & Minuman": ["Beli gorengan & kopi", "Makan siang bakso", "Beli nasi padang", "Jajan popmie"],
        "Transportasi": ["Naik gojek ke kampus", "Ongkos angkot", "Isi bensin motor", "Naik grab PP"],
        "Belanja": ["Belanja bulanan supermarket", "Beli baju kaos", "Beli perlengkapan mandi"],
        "Hiburan": ["Tiket bioskop XXI", "Langganan Spotify", "Top up game"],
        "Tagihan": ["Bayar listrik PLN", "Bayar kuota internet", "Bayar air PDAM"],
        "Kesehatan": ["Beli obat flu di apotek", "Beli vitamin C"],
        "Lainnya": ["Kas RT", "Beli barang fotokopi"]
    }
    
    records = []
    current_date = start_date
    
    while current_date <= end_date:
        if current_date.day in [1, 25]:
            records.append({
                "Tanggal": current_date.replace(hour=9, minute=0, second=0),
                "Jenis": TYPE_INCOME,
                "Kategori": "Gaji",
                "Jumlah": 12000000,
                "Catatan": "Transfer Gaji Bulanan Kantor",
                "Pesan Balasan": "Pemasukan tercatat"
            })
            
        if np.random.rand() < 0.08:
            records.append({
                "Tanggal": current_date.replace(hour=14, minute=30, second=0),
                "Jenis": TYPE_INCOME,
                "Kategori": "Freelance Project",
                "Jumlah": float(np.random.choice([1500000, 2500000, 4000000])),
                "Catatan": "Pembayaran Project Web Design Client",
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
            note = np.random.choice(sample_notes[cat])
            records.append({
                "Tanggal": current_date.replace(hour=hr, minute=mn, second=0),
                "Jenis": TYPE_EXPENSE,
                "Kategori": cat,
                "Jumlah": float(amt),
                "Catatan": note,
                "Pesan Balasan": "Catatan pengeluaran tersimpan"
            })
            
        current_date += timedelta(days=1)
        
    df = pd.DataFrame(records)
    return preprocess_data(df)
