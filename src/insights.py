import pandas as pd

#helpers

def _validate_df(df: pd.DataFrame):
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty or None.")


def _filter_by_month(df: pd.DataFrame, month: str) -> pd.DataFrame:
    """
    month: 'YYYY-MM' (recommended) or 'Mon-YYYY'
    """
    _validate_df(df)
    m = df["Date"].dt.to_period("M").astype(str)
    filtered = df[m == month]
    if filtered.empty:
        raise ValueError(f"No data available for month: {month}")
    return filtered


def _filter_by_date_range(df: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    _validate_df(df)
    if start_date > end_date:
        raise ValueError("start_date must be before end_date.")
    filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    if filtered.empty:
        raise ValueError("No data available for selected date range.")
    return filtered


#Total spend in month
def total_spend_in_month(df: pd.DataFrame, month: str) -> float:
    """Return total spend in a given month."""
    mdf = _filter_by_month(df, month)
    return float(mdf["Amount"].sum())

#Transaction count in a month
def transaction_count_in_month(df: pd.DataFrame, month: str) -> int:
    """Return number of transactions in a given month."""
    mdf = _filter_by_month(df, month)
    return int(len(mdf))

#Average transaction value in a month
def average_transaction_in_month(df: pd.DataFrame, month: str) -> float:
    """Return average transaction amount in a given month."""
    mdf = _filter_by_month(df, month)
    return float(mdf["Amount"].mean())

#Total spend in a date range
def total_spend_in_date_range(df: pd.DataFrame, start_date, end_date) -> float:
    """Return total spend between two dates."""
    rdf = _filter_by_date_range(df, start_date, end_date)
    return float(rdf["Amount"].sum())

#Top merchant in a month
def top_merchant_in_month(df: pd.DataFrame, month: str) -> dict:
    """
    Return top merchant and spend in a month.
    Output: {"merchant": str, "amount": float}
    """
    mdf = _filter_by_month(df, month)
    grp = mdf.groupby("Merchant")["Amount"].sum()
    merchant = grp.idxmax()
    amount = float(grp.max())
    return {"merchant": merchant, "amount": amount}

#Unique merchants in a month
def unique_merchants_in_month(df: pd.DataFrame, month: str) -> int:
    """Return number of unique merchants in a month."""
    mdf = _filter_by_month(df, month)
    return int(mdf["Merchant"].nunique())

#Top category in a month
def top_category_in_month(df: pd.DataFrame, month: str) -> dict:
    """
    Return top category and spend in a month.
    Output: {"category": str, "amount": float}
    """
    mdf = _filter_by_month(df, month)
    grp = mdf.groupby("Category")["Amount"].sum()
    category = grp.idxmax()
    amount = float(grp.max())
    return {"category": category, "amount": amount}

#Weekend vs weekday spend   
def weekend_vs_weekday_spend(df: pd.DataFrame, month: str | None = None) -> dict:
    """
    Compare weekend vs weekday spend.
    Output: {"Weekend": float, "Weekday": float, "dominant": str}
    """
    data = _filter_by_month(df, month) if month else df
    grp = data.groupby("Day_Type")["Amount"].sum()

    weekend = float(grp.get("Weekend", 0.0))
    weekday = float(grp.get("Weekday", 0.0))
    dominant = "Weekend" if weekend > weekday else "Weekday"

    return {
        "Weekend": weekend,
        "Weekday": weekday,
        "dominant": dominant
    }


#Highest spending week in a month
def highest_spending_week_in_month(df: pd.DataFrame, month: str) -> dict:
    """
    Return week with highest spend in a month.
    Output: {"week": int, "amount": float}
    """
    mdf = _filter_by_month(df, month)
    grp = mdf.groupby("Week_Number")["Amount"].sum()
    week = int(grp.idxmax())
    amount = float(grp.max())
    return {"week": week, "amount": amount}
