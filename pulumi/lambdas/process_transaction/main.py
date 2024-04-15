import json
import logging
import pandas
from transaction_processor import process_transactions, calculate_summary
from email_sender import format_summary_email

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    print("I am working")
    print(event)
