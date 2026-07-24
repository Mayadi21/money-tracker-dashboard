"""
Constants and design tokens for Money Tracker Dashboard
"""

# Color Palette
COLOR_PRIMARY = "#2563EB"   # Royal Blue
COLOR_SUCCESS = "#10B981"   # Emerald Green
COLOR_DANGER = "#EF4444"    # Bright Red
COLOR_WARNING = "#F59E0B"   # Amber Warning
COLOR_NEUTRAL = "#64748B"   # Slate Gray
COLOR_BG_LIGHT = "#F8FAFC"  # Light background
COLOR_CARD_BG = "#FFFFFF"

# Category Plotly Chart Color Map
CATEGORY_COLORS = {
    "Makanan & Minuman": "#F59E0B",
    "Transportasi": "#3B82F6",
    "Belanja": "#EC4899",
    "Hiburan": "#8B5CF6",
    "Tagihan": "#EF4444",
    "Kesehatan": "#10B981",
    "Proyek": "#06B6D4",
    "Gaji": "#10B981",
    "Freelance": "#6366F1",
    "Investasi": "#059669",
    "Lainnya": "#64748B"
}

# Standardized Transaction Types
TYPE_INCOME = "Pemasukan"
TYPE_EXPENSE = "Pengeluaran"

# Default Monthly Category Budgets (in IDR / Rp)
DEFAULT_CATEGORY_BUDGETS = {
    "Makanan & Minuman": 2500000,
    "Transportasi": 1500000,
    "Belanja": 2000000,
    "Hiburan": 1000000,
    "Tagihan": 3000000,
    "Kesehatan": 1000000,
    "Lainnya": 1000000
}

# Indonesian Day of Week Map
DAYS_INDONESIAN = {
    0: "Senin",
    1: "Selasa",
    2: "Rabu",
    3: "Kamis",
    4: "Jumat",
    5: "Sabtu",
    6: "Minggu"
}

# Indonesian Month Map
MONTHS_INDONESIAN = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}
