from typing import Any
import pandas as pd
from decimal import Decimal


def process_transactions(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file containing account transactions and returns a DataFrame.

    :param file_path: The path to the CSV file.
    :return: A DataFrame containing the transactions.
    """
    df = pd.read_csv(file_path)

    print(f"Proccessing dataframe {df.head(3)}")

    return df


def calculate_summary(df: pd.DataFrame) -> dict[str, Any]:
    """
    Calculates summary information for the account transactions.

    :param df: A DataFrame containing the transactions.
    :return: A dictionary with summary information.
    """
    # New dataframe
    new_df = pd.DataFrame(columns=["Amount", "Date", "Month", "Type"])

    # Conditionally convert to either positive or negative float
    new_df["Amount"] = df["Transaction"].apply(
        lambda x: (
            float(x[1:])
            if isinstance(x, str) and x[0] == "+"
            else -float(x[1:]) if isinstance(x, str) and x[0] == "-" else x
        )
    )

    # Format date
    new_df["Date"] = pd.to_datetime(df["Date"], format="%m/%d")
    new_df["Month"] = df["Date"].dt.strftime("%B")

    # Categorize transaction type
    new_df["Type"] = df["Amount"].apply(lambda x: "Credit" if float(x) > 0 else "Debit")

    # Summarize
    total_balance = df["Amount"].sum()
    num_transactions = df.groupby("Month").size().to_dict()
    avg_debit_amount = df[df["Type"] == "Debit"]["Amount"].mean()
    avg_credit_amount = df[df["Type"] == "Credit"]["Amount"].astype(float).mean()

    # Dynamically evaluate month in which there were transactions
    transactions = {
        f"{month}Transactions": f"{value:.0f}"
        for month, value in num_transactions.items()
    }

    result = {
        "total_balance": Decimal(total_balance),
        "avg_credit_amount": Decimal(avg_credit_amount),
        "avg_debit_amount": Decimal(avg_debit_amount),
        **transactions,
    }

    print(f"Got summary {result}")

    return result
