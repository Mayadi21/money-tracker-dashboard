"""
Formatting utilities for numbers, currencies, percentages, and dates
"""
import pandas as pd

def format_currency(val: float, symbol: str = "Rp ", compact: bool = False) -> str:
    """Format float or int into IDR currency string."""
    if pd.isna(val) or val is None:
        return f"{symbol}0"
    
    val = float(val)
    if compact:
        abs_val = abs(val)
        sign = "-" if val < 0 else ""
        if abs_val >= 1_000_000_000:
            return f"{sign}{symbol}{abs_val / 1_000_000_000:.2f}B"
        elif abs_val >= 1_000_000:
            return f"{sign}{symbol}{abs_val / 1_000_000:.1f}M"
        elif abs_val >= 1_000:
            return f"{sign}{symbol}{abs_val / 1_000:.0f}k"
    
    return f"{symbol}{val:,.0f}".replace(",", ".")

def format_percent(val: float, show_sign: bool = True) -> str:
    """Format float into percentage string."""
    if pd.isna(val) or val is None:
        return "0.0%"
    sign = "+" if (show_sign and val > 0) else ""
    return f"{sign}{val:.1f}%"

def format_date(dt, fmt: str = "%d %b %Y") -> str:
    """Format datetime object or timestamp into string."""
    if pd.isna(dt) or dt is None:
        return "-"
    try:
        return pd.to_datetime(dt).strftime(fmt)
    except Exception:
        return str(dt)

def get_trend_indicator(delta: float) -> tuple[str, str]:
    """
    Return indicator arrow symbol and CSS class based on numeric delta.
    (symbol, css_class)
    """
    if pd.isna(delta) or delta == 0:
        return "▬", "neutral"
    elif delta > 0:
        return "▲", "up-green"
    else:
        return "▼", "down-red"
