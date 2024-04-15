import os
import json
import boto3
from transaction_processor import process_transactions, calculate_summary
from email_sender import format_summary_email
from uuid import uuid4

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
account_table = dynamodb.Table(os.environ["ACCOUNT_TABLE_NAME"])
transactions_table = dynamodb.Table(os.environ["TRANSACTION_TABLE_NAME"])


def handler(event, context):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]
    temp_file_path = "/tmp/temp_transactions.csv"

    s3.download_file(bucket_name, object_key, temp_file_path)

    # This would obviously come directly in the data or from another system. Used to relate one entity to another
    account_id = str(uuid4())

    # Get current transactions and store them
    transactions_df = process_transactions(temp_file_path)
    with transactions_table.batch_writer() as batch:
        for index, row in transactions_df.iterrows():
            batch.put_item(
                Item={
                    "id": str(row["Id"]),
                    "date": str(row["Date"]),
                    "transaction": str(row["Transaction"]),
                    "account_id": account_id,
                }
            )

    # Get summary and store summary in db
    summary = calculate_summary(df=transactions_df, account_id=account_id)
    account_table.put_item(Item=summary)

    # Format summary for email
    formatted_summary = format_summary_email(summary)

    print(formatted_summary)
