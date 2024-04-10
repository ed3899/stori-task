from transaction_processor import process_transactions, calculate_summary
from email_sender import format_summary_email

# Process transactions
file_path = 'transactions.csv'
transactions_df = process_transactions(file_path)

# Calculate summary
summary = calculate_summary(transactions_df)
formatted_summary = format_summary_email(summary)

print(formatted_summary)