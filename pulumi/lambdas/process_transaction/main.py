import os
import json
import logging
import pandas as pd
import boto3
from botocore.config import Config
from transaction_processor import process_transactions, calculate_summary
from email_sender import format_summary_email

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
account_table = dynamodb.Table(os.environ["ACCOUNT_TABLE_NAME"])
transactions_table = dynamodb.Table(os.environ["TRANSACTION_TABLE_NAME"])
transactions_table_batch = transactions_table.batch_writer()


def handler(event, context):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]
    temp_file_path = "/tmp/temp_transactions.csv"

    s3.download_file(bucket_name, object_key, temp_file_path)

    # Get current transactions and store them
    transactions_df = process_transactions(temp_file_path)
    for index, row in transactions_df.iterrows():
        transactions_table_batch.put_item(
            Item={
                "Id": row["Id"],
                "Date": row["Date"],
                "Transaction": row["Transaction"],
            }
        )

    # Get summary and store summary in db
    summary = calculate_summary(transactions_df)
    account_table.put_item(summary)

    # Format summary for email
    formatted_summary = format_summary_email(summary)

    print(formatted_summary)
