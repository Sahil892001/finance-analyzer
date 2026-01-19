import streamlit as st
import pandas as pd
from pathlib import Path
from src.pdf_to_csv import pdf_to_dataframe
from src.data_enrichment import enrich
import tempfile
from src.charts import (
    plot_monthly_spending,
    plot_weekly_spending,
    plot_category_spending,
    plot_top_merchants,
    plot_day_of_week_spending,
    plot_spend_bucket_distribution,
    aggregate_data,
    plot_bar,
    plot_line,
)
from src.insights import (
    total_spend_in_month,
    transaction_count_in_month,
    average_transaction_in_month,
    top_merchant_in_month,
    top_category_in_month,
    weekend_vs_weekday_spend,
    highest_spending_week_in_month,
)


# --- App config ---
st.set_page_config(
    page_title="Finance Analyzer",
    layout="wide",
)

# --- Session state init ---
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "df" not in st.session_state:
    st.session_state.df = None


# =========================
# Landing Page
# =========================
def render_landing_page():
    col1, col2 = st.columns([1.3, 1])

    # --------------------
    # LEFT: Product intro + upload
    # --------------------
    with col1:
        st.title("Finance Analyzer")
        st.markdown(
            """
            Turn your **PhonePe transactions** into clear insights, charts, and answers — instantly.

            **What you get:**
            - Automatic spending analysis from your PDF
            - Clear charts showing where your money goes
            - Smart insights without manual calculations
            - Full transparency with enriched data you can download
            """
        )

        st.markdown("---")

        uploaded_file = st.file_uploader(
            "Upload your PhonePe transaction PDF",
            type=["pdf"]
        )

        analyze_clicked = st.button("Analyze My Spending")

        if analyze_clicked:
            if uploaded_file is None:
                st.warning("Please upload a PhonePe transaction PDF to continue.")
                return

            with st.spinner("Analyzing your transactions..."):
                # Save uploaded PDF temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                    tmp_pdf.write(uploaded_file.read())
                    temp_pdf_path = Path(tmp_pdf.name)

                # PDF → DataFrame
                raw_df = pdf_to_dataframe(temp_pdf_path)

                # Enrich data
                enriched_df = enrich(raw_df)

                # Store in session state
                st.session_state.df = enriched_df
                st.session_state.page = "dashboard"
                st.rerun()

    # --------------------
    # RIGHT: What user will see (tabs)
    # --------------------
    with col2:
        st.subheader("What you’ll discover")

        tab1, tab2, tab3 = st.tabs(["📈 Trends", "💡 Insights", "🎛️ Control"])

        with tab1:
            st.markdown(
                """
                **Understand your spending patterns over time**

                - Monthly and weekly spending trends
                - See how your expenses change over time
                - Identify high-spend periods instantly
                - Visual clarity instead of raw numbers

                These charts help you answer questions like:
                *“Am I spending more this month than last?”*
                """
            )

        with tab2:
            st.markdown(
                """
                **Get instant answers without digging into data**

                - Total spend for any month
                - Your top merchant and top category
                - Highest spending week
                - Weekend vs weekday spending behavior

                No charts needed — just **clear, direct answers**
                generated from your transaction history.
                """
            )

        with tab3:
            st.markdown(
                """
                **Explore your data your way**

                - Build custom charts using filters
                - Compare spending by category or merchant
                - Choose metrics like total, average, or count
                - Focus on specific months or date ranges

                This section is designed for **deeper exploration**
                when you want more control.
                """
            )



# =========================
# Dashboard Page
# =========================
def render_dashboard_page():
    st.sidebar.title("Finance Analyzer")

    if st.sidebar.button("🔄 Upload Another PDF"):
        # Clear session state
        st.session_state.df = None
        st.session_state.page = "landing"
        st.rerun()

    section = st.sidebar.radio(
        "Navigate",
        ["Dashboard", "Explore", "Quick Insights", "Data View"]
    )

    if st.session_state.df is None:
        st.warning("No data loaded. Please upload a PDF.")
        return

    df = st.session_state.df

    # -------- Dashboard --------
    if section == "Dashboard":
        st.header("Dashboard")

        st.subheader("Summary")

        col1, col2, col3, col4 = st.columns(4)

        total_spend = df["Amount"].sum()
        total_txns = len(df)
        avg_txn = df["Amount"].mean()
        credit_total = df.loc[df["Type"] == "CREDIT", "Amount"].sum()

        with col1:
            st.metric("Total Spend", f"₹{total_spend:,.0f}")

        with col2:
            st.metric("Transactions", f"{total_txns}")

        with col3:
            st.metric("Avg Transaction", f"₹{avg_txn:,.0f}")

        with col4:
            st.metric("Total Credit", f"₹{credit_total:,.0f}")

        st.subheader("Spending Overview")

        # ---- Row 1 ----
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Monthly Spending Trend**")
            try:
                fig = plot_monthly_spending(df)
                st.pyplot(fig, use_container_width=True)
            except Exception as e:
                st.error("Unable to generate monthly spending chart.")
                st.exception(e)

        with col2:
            st.markdown("**Weekly Spending Trend**")
            try:
                fig = plot_weekly_spending(df)
                st.pyplot(fig, use_container_width=True)
            except Exception as e:
                st.error("Unable to generate weekly spending chart.")
                st.exception(e)


        # ---- Row 2 ----
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("**Category-wise Spending**")
            try:
                fig = plot_category_spending(df)
                st.pyplot(fig, use_container_width=True)
            except Exception as e:
                st.error("Unable to generate category spending chart.")
                st.exception(e)

        with col4:
            st.markdown("**Top Merchants by Spend**")
            try:
                fig = plot_top_merchants(df)
                st.pyplot(fig, use_container_width=True)
            except Exception as e:
                st.error("Unable to generate top merchants chart.")
                st.exception(e)


        # ---- Row 3 ----
        col5, col6 = st.columns(2)

        with col5:
            st.markdown("**Spending by Day of Week**")
            try:
                fig = plot_day_of_week_spending(df)
                st.pyplot(fig, use_container_width=True)
            except Exception as e:
                st.error("Unable to generate day-of-week chart.")
                st.exception(e)

        with col6:
            st.markdown("**Spend Bucket Distribution**")
            try:
                fig = plot_spend_bucket_distribution(df)
                st.pyplot(fig, use_container_width=True)
            except Exception as e:
                st.error("Unable to generate spend bucket chart.")
                st.exception(e)



    # -------- Explore --------
    elif section == "Explore":
        st.header("Explore")
        st.markdown(
            "Create custom charts by selecting how you want to filter, group, and analyze your data."
        )

        # --------------------
        # Controls
        # --------------------
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            time_mode = st.selectbox(
                "Time Filter",
                ["All Data", "Single Month", "Date Range"]
            )

        with col2:
            group_by = st.selectbox(
                "Group By",
                ["Category", "Merchant", "SpendBucket", "Day_Of_Week", "Week_Number"]
            )

        with col3:
            metric_label = st.selectbox(
                "Metric",
                ["Total Spend", "Transaction Count", "Average Spend"]
            )

        with col4:
            chart_type = st.selectbox(
                "Chart Type",
                ["Bar", "Horizontal Bar", "Line"]
            )

        # --------------------
        # Time filtering
        # --------------------
        filtered_df = df.copy()

        if time_mode == "Single Month":
            month = st.selectbox("Select Month", sorted(df["Month"].unique()))
            filtered_df = df[df["Month"] == month]

        elif time_mode == "Date Range":
            start_date = st.date_input("Start Date", df["Date"].min())
            end_date = st.date_input("End Date", df["Date"].max())

            if start_date > end_date:
                st.error("Start date must be before end date.")
                st.stop()

            filtered_df = df[
                (df["Date"].dt.date >= start_date) &
                (df["Date"].dt.date <= end_date)
            ]

        # --------------------
        # Metric mapping
        # --------------------
        metric_map = {
            "Total Spend": "sum",
            "Transaction Count": "count",
            "Average Spend": "mean",
        }
        metric = metric_map[metric_label]

        # --------------------
        # Generate chart
        # --------------------
        generate = st.button("Generate Chart")

        if generate:
            if filtered_df.empty:
                st.warning("No data available for the selected filters.")
                st.stop()

            # Line chart validation
            if chart_type == "Line" and group_by not in ["Week_Number", "Day_Of_Week"]:
                st.warning("Line charts are only supported for time-based groupings.")
                st.stop()

            try:
                # Aggregate
                aggregated = aggregate_data(filtered_df, group_by, metric)

                # Plot
                if chart_type == "Bar":
                    fig = plot_bar(
                        aggregated,
                        title=f"{metric_label} by {group_by}",
                        ylabel=metric_label,
                        horizontal=False
                    )

                elif chart_type == "Horizontal Bar":
                    fig = plot_bar(
                        aggregated,
                        title=f"{metric_label} by {group_by}",
                        ylabel=metric_label,
                        horizontal=True
                    )

                else:  # Line chart
                    fig = plot_line(
                        aggregated.index,
                        aggregated.values,
                        title=f"{metric_label} by {group_by}",
                        xlabel=group_by,
                        ylabel=metric_label
                    )

                st.pyplot(fig, use_container_width=True)

            except Exception as e:
                st.error("Unable to generate chart.")
                st.exception(e)




    # -------- Quick Insights --------
    elif section == "Quick Insights":
        st.header("Quick Insights")

        # Month selector (use existing Month column)
        months = sorted(df["Month"].dropna().unique())
        selected_month = st.selectbox("Select Month", months)

        try:
            total_spend = total_spend_in_month(df, selected_month)
            txn_count = transaction_count_in_month(df, selected_month)
            avg_txn = average_transaction_in_month(df, selected_month)

            top_merchant = top_merchant_in_month(df, selected_month)
            top_category = top_category_in_month(df, selected_month)
            top_week = highest_spending_week_in_month(df, selected_month)
            weekend_weekday = weekend_vs_weekday_spend(df, selected_month)

            col1, col2, col3 = st.columns(3)

            # ---- Column 1 ----
            with col1:
                st.metric("Total Spend", f"₹{total_spend:,.0f}")
                st.metric("Transactions", txn_count)
                st.metric("Avg Transaction", f"₹{avg_txn:,.0f}")

            # ---- Column 2 ----
            with col2:
                st.metric(
                    "Top Merchant",
                    top_merchant["merchant"],
                    f"₹{top_merchant['amount']:,.0f}"
                )
                st.metric(
                    "Top Category",
                    top_category["category"],
                    f"₹{top_category['amount']:,.0f}"
                )

            # ---- Column 3 ----
            with col3:
                st.metric(
                    "Highest Spend Week",
                    f"Week {top_week['week']}",
                    f"₹{top_week['amount']:,.0f}"
                )
                st.metric(
                    "Weekend vs Weekday",
                    weekend_weekday["dominant"],
                )

        except ValueError as e:
            st.warning(str(e))


    # -------- Data View --------
    elif section == "Data View":
        st.header("Data View")

        display_df = df.copy()
        display_df["Date"] = display_df["Date"].dt.date

        st.dataframe(display_df, use_container_width=True)

        st.download_button(
            label="Download Enriched Data (CSV)",
            data=display_df.to_csv(index=False),
            file_name="phonepe_enriched_data.csv",
            mime="text/csv"
        )


# =========================
# Main Router
# =========================
if st.session_state.page == "landing":
    render_landing_page()
else:
    render_dashboard_page()

