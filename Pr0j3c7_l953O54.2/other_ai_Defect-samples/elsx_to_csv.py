import pandas as pd

# Load the Excel file
excel_file = 'records_docs/haraka50seeds.xlsx'

# Read the Excel file
df = pd.read_excel(excel_file)

# Save to CSV
csv_file = 'records_docs/haraka50seeds.xlsx.csv'
df.to_csv(csv_file, index=False)
