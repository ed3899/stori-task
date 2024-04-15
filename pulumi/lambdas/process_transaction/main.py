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


def handler(event, context):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]

    s3.download_file(bucket_name, object_key, "/tmp/temp_transactions.csv")

    transactions_df = process_transactions("/tmp/temp_transactions.csv")
    summary = calculate_summary(transactions_df)
    formatted_summary = format_summary_email(summary)

    print(formatted_summary)
