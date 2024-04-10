from typing import Any
import pandas as pd


def process_transactions(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file containing account transactions and returns a DataFrame.

    :param file_path: The path to the CSV file.
    :return: A DataFrame containing the transactions.
    """
    df = pd.read_csv(file_path)
    return df


def calculate_summary(df: pd.DataFrame) -> dict[str, Any]:
    """
    Calculates summary information for the account transactions.

    :param df: A DataFrame containing the transactions.
    :return: A dictionary with summary information.
    """
    # Conditionally convert to either positive or negative float
    df["Amount"] = df["Transaction"].apply(
        lambda x: (
            float(x[1:])
            if isinstance(x, str) and x[0] == "+"
            else -float(x[1:]) if isinstance(x, str) and x[0] == "-" else x
        )
    )
    # Format date
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d")
    df["Month"] = df["Date"].dt.strftime("%B")

    total_balance = df["Amount"].sum()
    num_transactions = df.groupby("Month").size().to_dict()

    return {
        "Total balance": total_balance,
        "Number of transactions": num_transactions,
    }
