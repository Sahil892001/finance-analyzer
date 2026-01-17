import pandas as pd
import matplotlib.pyplot as plt

# Monthly spending trend
def plot_monthly_spending(df: pd.DataFrame):
    monthly = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum()
    monthly.index = monthly.index.astype(str)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(monthly.index, monthly.values, marker="o")
    ax.set_title("Monthly Spending Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Spend")
    ax.grid(True)
    plt.xticks(rotation=45)

    return fig

#Weekly spending trend
def plot_weekly_spending(df: pd.DataFrame):
    weekly = df.groupby("Week_Number")["Amount"].sum().sort_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(weekly.index, weekly.values, marker="o")
    ax.set_title("Weekly Spending Trend")
    ax.set_xlabel("Week Number")
    ax.set_ylabel("Total Spend")
    ax.grid(True)

    return fig


#Category-wise spending
def plot_category_spending(df: pd.DataFrame):
    category = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 4))
    category.plot(kind="bar", ax=ax)
    ax.set_title("Spending by Category")
    ax.set_ylabel("Total Spend")
    plt.xticks(rotation=45)

    return fig


#Top Merchants by Spend
def plot_top_merchants(df: pd.DataFrame, top_n: int = 10):
    merchants = (
        df.groupby("Merchant")["Amount"]
          .sum()
          .sort_values(ascending=False)
          .head(top_n)
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    merchants.plot(kind="barh", ax=ax)
    ax.set_title(f"Top {top_n} Merchants by Spend")
    ax.set_xlabel("Total Spend")
    ax.invert_yaxis()

    return fig

#Spending by Day of Week
def plot_day_of_week_spending(df: pd.DataFrame):
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dow = df.groupby("Day_Of_Week")["Amount"].sum().reindex(order)

    fig, ax = plt.subplots(figsize=(7, 4))
    dow.plot(kind="bar", ax=ax)
    ax.set_title("Spending by Day of Week")
    ax.set_ylabel("Total Spend")

    return fig


#Spend Bucket Distribution
def plot_spend_bucket_distribution(df: pd.DataFrame):
    bucket = df.groupby("SpendBucket")["Amount"].count()

    fig, ax = plt.subplots(figsize=(6, 4))
    bucket.plot(kind="bar", ax=ax)
    ax.set_title("Transaction Count by Spend Bucket")
    ax.set_ylabel("Number of Transactions")

    return fig