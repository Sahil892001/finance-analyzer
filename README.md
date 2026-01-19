# 📊 Finance Analyzer

  

Finance Analyzer is a **Streamlit-based data analysis application** that transforms **PhonePe transaction PDFs** into meaningful insights, charts, and summaries.

It automates data extraction, enrichment, and visualization, allowing users to understand their spending patterns without manual effort.

---

## ✨ Key Features
 

- 📄 Upload PhonePe transaction PDF and analyze instantly

- 🧹 Automatic data enrichment (dates, categories, spend buckets, weekends, etc.)

- 📊 Interactive dashboard with default spending charts

- 💡 Quick Insights section for direct numeric answers (monthly spend, top merchant, etc.)

- 🔍 Explore section to build custom charts using filters and metrics

- 📑 View and download the enriched dataset as CSV

  

---

  

## 🧠 What the App Does

  

1.  **PDF Processing**

  - Extracts transaction data from PhonePe PDFs using `pdfplumber`

  

2.  **Data Enrichment**

- Adds analytical columns like:

- Month, Day, Day of Week

- Week Number

- Spend Buckets

- Categories

- Weekend vs Weekday flags

  

3.  **Analysis & Visualization**

- Default charts: monthly trends, weekly trends, category split, top merchants, etc.

- User-driven custom charts via Explore section

- Instant numeric insights without charts

  

4.  **Transparency**

- Users can inspect the full enriched dataset

- CSV download available directly from the UI

  

---

  

## 🖥️ Application Sections

  

-  **Landing Page** – Upload PDF and understand what the app provides

-  **Dashboard** – Summary metrics and default charts

-  **Quick Insights** – Direct answers for common financial questions

-  **Explore** – Build custom charts with filters and metrics

-  **Data View** – Tabular view of enriched data with CSV download

  

---

  

## 🛠️ Tech Stack

  

-  **Python**

-  **Pandas & NumPy** – data processing

-  **Matplotlib** – chart generation

-  **Streamlit** – frontend & interactivity

-  **pdfplumber** – PDF parsing

  

---

  

## ▶️ How to Run Locally

  

### Clone the repository

git clone <your-repo-url>
cd Finance-Project  

### Create & activate virtual environment
python -m venv venv
venv\Scripts\activate
source venv/bin/activate (for mac/linux)

### Install dependencies
pip install -r requirements.txt

### Run the application
streamlit run app.py
The app will open at:

http://localhost:8501

## Data Privacy

Uploaded PDFs are processed locally

No data is stored or sent externally

Temporary files are ignored using .gitignore




## Future Improvements
Export insights as PDF reports

Support multiple PDFs at once

Monthly or yearly spending comparisons

Spending anomaly detection
