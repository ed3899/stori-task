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


def object_url(bucket_name: str, key: str):
    return f"https://{bucket_name}.s3.amazonaws.com/{key}"


def handler(event, context):
    bucket_name: str = event["Records"][0]["s3"]["bucket"]["name"]
    object_key: str = event["Records"][0]["s3"]["object"]["key"]
    temp_file_path = "/tmp/temp_transactions.csv"
    stori_logo_url = object_url(bucket_name=bucket_name, key="stori_logo.jpg")

    if not object_key.endswith(".csv"):
        return

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
    formatted_summary = format_summary_email(summary, logo_url=stori_logo_url)

    # Convert the MIMEText object to a string
    plain_content_str = formatted_summary.as_string()

    # Create the response body as a list containing the MIMEText string
    response_body = [plain_content_str]

    # Convert the response body to JSON
    response_json = json.dumps(response_body)

    result = {
        "statusCode": 201,
        "body": response_json,
        "headers": {"Content-Type": "application/json"},
    }

    print(f"Final result {result}")

    return result
