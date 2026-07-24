"""
Dataframe filtering functions
"""
import pandas as pd
from typing import Tuple, List, Optional
from datetime import date

def filter_dataframe(
    df: pd.DataFrame,
    date_range: Optional[Tuple[date, date]] = None,
    years: Optional[List[int]] = None,
    months: Optional[List[int]] = None,
    tx_type: str = "All",
    categories: Optional[List[str]] = None,
    search_query: str = ""
) -> pd.DataFrame:
    """Filter transactions dataframe according to sidebar control parameters."""
    if df.empty:
        return df.copy()
        
    filtered = df.copy()
    
    # 1. Date Range Filter
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        if start_date and end_date:
            filtered = filtered[
                (filtered["DateOnly"] >= start_date) & 
                (filtered["DateOnly"] <= end_date)
            ]
            
    # 2. Year Filter
    if years and len(years) > 0:
        filtered = filtered[filtered["Year"].isin(years)]
        
    # 3. Month Filter
    if months and len(months) > 0:
        filtered = filtered[filtered["Month"].isin(months)]
        
    # 4. Transaction Type Filter
    if tx_type and tx_type != "All":
        filtered = filtered[filtered["Jenis"] == tx_type]
        
    # 5. Category Filter
    if categories and len(categories) > 0:
        filtered = filtered[filtered["Kategori"].isin(categories)]
        
    # 6. Text Search Filter
    if search_query.strip():
        q = search_query.strip().lower()
        cat_match = filtered["Kategori"].str.lower().str.contains(q, na=False)
        note_match = filtered["Catatan"].str.lower().str.contains(q, na=False)
        filtered = filtered[cat_match | note_match]
        
    return filtered
