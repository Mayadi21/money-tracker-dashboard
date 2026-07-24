# 💸 Money Tracker Dashboard

A modern, premium personal finance application built with **Python**, **Streamlit**, **Pandas**, and **Plotly**. Inspired by leading fintech applications (Wallet, YNAB, Spendee, Mint), this dashboard simplifies personal finance tracking with dynamic visualizations, cumulative cash flow trends, and decision-focused financial metrics.

---

## ✨ Key Features

- **📅 Predefined Date Range Presets**: Easily switch between **Current Month** (Default), **Last 30 Days**, **Year To Date**, **All Time**, and **Custom Range**.
- **💳 3 Primary Financial KPI Cards**:
  - **Total Income** (with income transaction count)
  - **Total Expense** (with expense transaction count)
  - **Net Cash Flow** (Income - Expense)
- **📈 Hero Cumulative Cash Flow Chart**:
  - Plotly interactive line chart showcasing **Cumulative Running Totals** over time.
  - Granularity level selector (**Daily | Weekly | Monthly**).
  - Smooth curves with markers, hover tooltips, and formatted Rupiah currency (`Rp`).
- **🍩 Dual Donut Category Charts**:
  - **Income Distribution**: *"Where does my income come from?"*
  - **Expense Distribution**: *"Where does my money go?"*
  - Displays total center annotations, percentages, and category values.
- **📋 Interactive Transaction Table**: Search, filter by category/type, sort chronologically, and export filtered transactions to CSV with a single click.
- **🔒 Secure Credentials Management**: Integrates with Streamlit secrets (`.streamlit/secrets.toml`) to prevent hardcoding sensitive Google Sheet IDs in public repositories.


---

## 📁 Project Structure

```
money_tracker_v2/
├── app.py                      # Main Streamlit application entrypoint & layout
├── requirements.txt            # Python package dependencies
├── assets/
│   └── styles.css              # Custom CSS tokens (typography, cards, badges)
├── components/
│   ├── header.py              # Header component
│   ├── date_filter.py         # Date preset selector (Current Month, YTD, 30D, etc.)
│   ├── metric_cards.py        # Primary 3 KPI summary cards
│   ├── cashflow_chart.py      # Hero cumulative cash flow line chart
│   ├── donut_charts.py        # Side-by-side Dual Donut category charts
│   ├── transaction_table.py   # Recent transactions table with CSV download
│   └── sidebar.py             # Category & search filters
├── utils/
│   ├── data_loader.py         # Data loading, Streamlit secrets resolution & fallback
│   ├── aggregation.py        # Cached time series aggregations (Daily, Weekly, Monthly)
│   ├── statistics.py          # Financial metric calculations & deltas
│   ├── formatter.py           # IDR currency, percentage, and date formatters
│   ├── filters.py             # Vectorized pandas filtering
│   ├── constants.py           # Color palettes and default constants
│   └── helpers.py             # UI helpers and CSS loader
└── .streamlit/
    ├── secrets.toml.example   # Public template for secrets configuration
    └── secrets.toml           # Local private secrets configuration (git-ignored)
```

---

## ⚙️ Configuration Setup

### Option 1: Using Google Sheets (Recommended)

1. Create a Google Sheet with the following columns:
   - `Tanggal` (Format: `DD/MM/YYYY HH:MM:SS`)
   - `Jenis` (`Pemasukan` or `Pengeluaran`)
   - `Kategori` (e.g., `Food & Beverage`, `Transportation`, `Salary`, etc.)
   - `Jumlah` (Numeric amount)
   - `Catatan` [Optional]
   - `Pesan Balasan` [Optional]

2. Share your Google Sheet set to **"Anyone with the link can view"**.

3. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

4. Open `.streamlit/secrets.toml` and paste your Google Sheet ID or CSV Export URL:
   ```toml
   [google_sheets]
   sheet_id = "YOUR_GOOGLE_SHEET_ID_HERE"
   csv_url = "https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEET_ID_HERE/export?format=csv"
   ```

### Option 2: Demo Mode (No Setup Required)
If no `secrets.toml` or invalid Google Sheet URL is provided, the application automatically launches in **Demo Mode** using realistic generated sample data.

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/Mayadi21/money-tracker-dashboard.git
cd money-tracker-dashboard
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv .tracker_env
.tracker_env\Scripts\activate

# macOS / Linux
python3 -m venv .tracker_env
source .tracker_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Streamlit App
```bash
streamlit run app.py
```

The application will open automatically in your default web browser at `http://localhost:8501`.

---

## 🛠️ Tech Stack

- **Framework**: [Streamlit](https://streamlit.io/)
- **Data Processing**: [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)
- **Visualizations**: [Plotly Express](https://plotly.com/python/) & [Plotly Graph Objects](https://plotly.com/python/graph-objects/)
- **Styling**: Vanilla CSS (Custom Design Tokens)
- **Python Version**: 3.9+

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
