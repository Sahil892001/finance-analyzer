#!/usr/bin/env python3
"""
Finance Data Enrichment for Finance Analyzer Project.

Usage (CLI):
    python finance_data_enrich.py --input data/phonepe_spendings.csv --output data/phonepe_spendings_enriched.csv
"""

from __future__ import annotations
import argparse
import logging
from pathlib import Path
import re
from typing import Dict, Optional

import pandas as pd
import numpy as np

# --- logging ---------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("finance_data_enrich")

# --- defaults & config -----------------------------------------------------
DEFAULT_INPUT = Path("../data/phonepe_spendings.csv")
DEFAULT_OUTPUT = Path("../data/phonepe_spendings_enriched.csv")

SPEND_BUCKETS = [
    (0, 300, "Small"),
    (300, 1000, "Medium"),
    (1000, float("inf"), "Large"),
]

# Basic merchant keyword->category map (extend as you observe merchants)
DEFAULT_CATEGORY_MAP: Dict[str, str] = {
    "swiggy": "Food",
    "zomato": "Food",
    "dominos": "Food",
    "uber": "Transport",
    "ola": "Transport",
    "amazon": "Shopping",
    "flipkart": "Shopping",
    "netflix": "Entertainment",
    "spotify": "Entertainment",
    "pharm": "Personal",
    "clinic": "Personal",
    # add new rules as needed
}

# --- helpers ---------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Enrich PhonePe transaction CSV into analysis-ready CSV")
    p.add_argument("--input", "-i", type=Path, default=DEFAULT_INPUT, help="Input CSV path")
    p.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT, help="Output enriched CSV path")
    p.add_argument("--overwrite", action="store_true", help="Overwrite existing output file if present")
    return p.parse_args()


def ensure_input_exists(path: Path) -> None:
    if not path.exists():
        logger.error("Input file not found: %s", path)
        raise FileNotFoundError(path)


def load_csv(path: Path) -> pd.DataFrame:
    logger.info("Loading CSV: %s", path)
    return pd.read_csv(path)


def safe_to_float(x) -> float:
    if pd.isna(x):
        return 0.0
    s = str(x)
    # remove non-numeric except minus and dot
    s = re.sub(r"[^0-9\.-]", "", s)
    try:
        return float(s)
    except Exception:
        return 0.0


def normalize_merchant(merchant: Optional[str]) -> str:
    if merchant is None or (isinstance(merchant, float) and np.isnan(merchant)):
        return ""
    s = str(merchant).strip()
    return re.sub(r"\s+", " ", s)


def map_spend_bucket(amount: float) -> str:
    for lo, hi, label in SPEND_BUCKETS:
        if lo <= amount <= hi:
            return label
    return "Unknown"


def map_category(merchant: str, category_map: Dict[str, str]) -> str:
    m = merchant.lower()
    for k, v in category_map.items():
        if k in m:
            return v
    # fallback heuristics
    food_kw = ["hotel", "restaurant", "cafe", "dhaba", "snack", "tea", "coffee", "bakery", "juice", "dine"]
    if any(kw in m for kw in food_kw):
        return "Food"
    return "Other"

# --- core enrichment pipeline ----------------------------------------------
def enrich(df: pd.DataFrame, category_map: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    df = df.copy()
    category_map = category_map or DEFAULT_CATEGORY_MAP

    # Ensure required columns exist
    for col in ["Date", "Merchant", "Type", "Amount"]:
        if col not in df.columns:
            logger.warning("Column '%s' missing from input; creating empty values.", col)
            df[col] = pd.NA

    # Parse Date
    logger.info("Parsing Date column to datetime")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)

    # Derived fields
    df["Month"] = df["Date"].dt.strftime("%b-%Y")
    df["Day"] = df["Date"].dt.day.fillna(0).astype(int)
    df["Day_Of_Week"] = df["Date"].dt.day_name()
    df["Week_Number"] = df["Date"].dt.isocalendar().week.astype("UInt32")

    # Normalize merchant and amount
    df["Merchant"] = df["Merchant"].apply(normalize_merchant)
    df["Amount"] = df["Amount"].apply(safe_to_float).astype(float)

    # Spend bucket & Category
    df["SpendBucket"] = df["Amount"].apply(map_spend_bucket)
    df["Category"] = df["Merchant"].apply(lambda m: map_category(m, category_map))

    # Weekend flag
    df["Is_Weekend"] = df["Day_Of_Week"].isin(["Saturday", "Sunday"]).astype(bool)
    df["Day_Type"] = np.where(df["Is_Weekend"], "Weekend", "Weekday")

    # Select ordered columns
    out_cols = [
        "Date",
        "Merchant",
        "Type",
        "Amount",
        "Month",
        "Day",
        "Day_Of_Week",
        "Week_Number",
        "SpendBucket",
        "Category",
        "Is_Weekend",
        "Day_Type",
    ]
    remaining = [c for c in df.columns if c not in out_cols]
    return df[out_cols + remaining].copy()


def save_csv(df: pd.DataFrame, path: Path, overwrite: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        logger.error("Output file %s exists. Use --overwrite to replace.", path)
        raise FileExistsError(path)
    df.to_csv(path, index=False)
    logger.info("Enriched CSV written to %s", path)


# --- CLI main --------------------------------------------------------------
def main() -> None:
    args = parse_args()
    try:
        ensure_input_exists(args.input)
        df_raw = load_csv(args.input)
        df_enriched = enrich(df_raw)
        save_csv(df_enriched, args.output, overwrite=args.overwrite)
    except Exception as exc:
        logger.exception("Failed to run enrichment: %s", exc)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
