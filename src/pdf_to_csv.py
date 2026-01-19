import pdfplumber
import pandas as pd
import re
from pathlib import Path
import tempfile

def pdf_to_csv(pdf_path: str, csv_path: str):
    """Extract PhonePe transactions from PDF and save them to CSV."""
    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for line in page.extract_text().split('\n'):
                if re.match(r"[A-Za-z]{3,4}\s\d{2}", line) and not line.startswith("Page"):
                    match = re.match(
                        r"([A-Za-z]{3,4}\s\d{1,2},\s20\d{2})+\sPaid to (.+?)\s+(DEBIT|CREDIT)\s*₹([\d,]+)",
                        line
                    )
                    if match:
                        date, merchant, txn_type, amount = match.groups()
                        transactions.append({
                            "Date": date,
                            "Merchant": merchant.strip(),
                            "Type": txn_type,
                            "Amount": float(amount.replace(",", ""))
                        })

    pd.DataFrame(transactions).to_csv(csv_path, index=False)


def pdf_to_dataframe(pdf_path):
    """
    Convert PhonePe PDF directly into a DataFrame (Streamlit-friendly).
    """
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        temp_csv_path = Path(tmp.name)

    pdf_to_csv(pdf_path, temp_csv_path)
    df = pd.read_csv(temp_csv_path)

    return df





if __name__ == "__main__":
    pdf_path = r"C:\Users\Administrator\Desktop\Finance Project\data\phonepe_spendings.pdf"
    csv_path = r"C:\Users\Administrator\Desktop\Finance Project\data\phonepe_spendings.csv"
    pdf_to_csv(pdf_path, csv_path)