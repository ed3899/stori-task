from transaction_processor import process_transactions, calculate_summary

# Process transactions
file_path = 'transactions.csv'
transactions_df = process_transactions(file_path)

# Calculate summary
summary = calculate_summary(transactions_df)

print(summary)