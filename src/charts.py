import pandas as pd
import matplotlib.pyplot as plt
DEFAULT_FIGSIZE = (10, 6)

def _validate_df(df):
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty or None.")


def _validate_date_range(start_date, end_date):
    if start_date > end_date:
        raise ValueError("start_date must be before end_date.")


# Monthly spending trend
def plot_monthly_spending(df: pd.DataFrame):
    _validate_df(df)

    monthly = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum()
    monthly.index = monthly.index.astype(str)

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    ax.plot(monthly.index, monthly.values, marker="o")
    ax.set_title("Monthly Spending Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Spend")
    ax.grid(True)
    plt.xticks(rotation=45)
    fig.set_constrained_layout(True)

    return fig

#Weekly spending trend
def plot_weekly_spending(df: pd.DataFrame):
    _validate_df(df)
    weekly = df.groupby("Week_Number")["Amount"].sum().sort_index()

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    ax.plot(weekly.index, weekly.values, marker="o")
    ax.set_title("Weekly Spending Trend")
    ax.set_xlabel("Week Number")
    ax.set_ylabel("Total Spend")
    ax.grid(True)
    fig.set_constrained_layout(True)

    return fig


#Category-wise spending
def plot_category_spending(df: pd.DataFrame):
    _validate_df(df)
    category = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    category.plot(kind="bar", ax=ax)
    ax.set_title("Spending by Category")
    ax.set_ylabel("Total Spend")
    plt.xticks(rotation=45)
    fig.set_constrained_layout(True)

    return fig


#Top Merchants by Spend
def plot_top_merchants(df: pd.DataFrame, top_n: int = 10):
    _validate_df(df)
    merchants = (
        df.groupby("Merchant")["Amount"]
          .sum()
          .sort_values(ascending=False)
          .head(top_n)
    )

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    merchants.plot(kind="barh", ax=ax)
    ax.set_title(f"Top {top_n} Merchants by Spend")
    ax.set_xlabel("Total Spend")
    ax.invert_yaxis()
    fig.set_constrained_layout(True)

    return fig

#Spending by Day of Week
def plot_day_of_week_spending(df: pd.DataFrame):
    _validate_df(df)
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dow = df.groupby("Day_Of_Week")["Amount"].sum().reindex(order)

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    dow.plot(kind="bar", ax=ax)
    ax.set_title("Spending by Day of Week")
    ax.set_ylabel("Total Spend")
    fig.set_constrained_layout(True)

    return fig


#Spend Bucket Distribution
def plot_spend_bucket_distribution(df: pd.DataFrame):
    _validate_df(df)
    bucket = df.groupby("SpendBucket")["Amount"].count()

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    bucket.plot(kind="bar", ax=ax)
    ax.set_title("Transaction Count by Spend Bucket")
    ax.set_ylabel("Number of Transactions")
    fig.set_constrained_layout(True)

    return fig


# Data filtering helpers

def filter_by_month(df, month_str):
    """
    month_str: '2025-03' or 'Mar-2025'
    """
    _validate_df(df)
    return df[df["Date"].dt.to_period("M").astype(str) == month_str]


def filter_by_date_range(df, start_date, end_date):
    _validate_df(df)
    return df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]


def filter_by_weeks(df, weeks):
    """
    weeks: list[int] e.g. [12, 13, 15]
    """
    _validate_df(df)
    return df[df["Week_Number"].isin(weeks)]


# Data Aggregation
def aggregate_data(df, group_by, metric):
    """
    group_by: 'Merchant', 'Category', 'Week_Number', 'Day_Of_Week', 'SpendBucket'
    metric: 'sum', 'count', 'mean'
    """
    _validate_df(df)

    if metric not in {"sum", "count", "mean"}:
        raise ValueError("metric must be one of: 'sum', 'count', 'mean'")


    if metric == "sum":
        return df.groupby(group_by)["Amount"].sum()
    elif metric == "count":
        return df.groupby(group_by).size()
    elif metric == "mean":
        return df.groupby(group_by)["Amount"].mean()
    else:
        raise ValueError("Invalid metric")


# Generic bar chart builder
def plot_bar(series, title, xlabel="", ylabel="", horizontal=False, top_n=None):

    if top_n:
        series = series.sort_values(ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)

    if horizontal:
        series.sort_values().plot(kind="barh", ax=ax)
    else:
        series.sort_values(ascending=False).plot(kind="bar", ax=ax)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.set_constrained_layout(True)

    return fig


#Generic line chart builder
def plot_line(x, y, title, xlabel="", ylabel=""):
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    ax.plot(x, y, marker="o")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    fig.set_constrained_layout(True)
    return fig


#Monthly data 
def plot_monthly_top_entities(df, month, group_by="Merchant", metric="sum", top_n=10):
    _validate_df(df)

    filtered = filter_by_month(df, month)
    agg = aggregate_data(filtered, group_by, metric)

    return plot_bar(
        agg,
        title=f"Top {top_n} {group_by}s in {month}",
        ylabel="Amount" if metric == "sum" else "Count",
        horizontal=True,
        top_n=top_n
    )


#Date range trend
def plot_date_range_trend(df, start_date, end_date):
    _validate_df(df)
    _validate_date_range(start_date, end_date)

    filtered = filter_by_date_range(df, start_date, end_date)
    daily = filtered.groupby("Date")["Amount"].sum()

    return plot_line(
        daily.index,
        daily.values,
        title="Spending Trend (Selected Date Range)",
        xlabel="Date",
        ylabel="Total Spend"
    )


#Week comparison
def plot_week_comparison(df, weeks, metric="sum"):
    _validate_df(df)

    filtered = filter_by_weeks(df, weeks)
    agg = aggregate_data(filtered, "Week_Number", metric)

    return plot_bar(
        agg,
        title="Week-wise Comparison",
        xlabel="Week Number",
        ylabel="Amount" if metric == "sum" else "Count"
    )


