import os
import pdfplumber
import pandas as pd
import re
from tabulate import tabulate


# Define paths for PDF input and output directory
pdf_path = "/home/Documents/py/Python/Oseberg/Garfiled_County/TGP_OutageImpactReport.pdf"
output_dir = "/home/Documents/py/Python/Oseberg/Garfiled_County/csvs/"

os.makedirs(output_dir, exist_ok=True)

def extract_tables_per_page(pdf_path, output_dir):
    """Extracts tables from each page and saves them as individual CSV files."""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            table = page.extract_table()
            if table and len(table) > 4:
                table = table[4:]  # Skip the first 4 rows
                # Determine headers if the first row contains valid headers
                headers = table[0] if all(cell is not None for cell in table[0]) and not all(isinstance(h, str) and h.isdigit() for h in table[0]) else None
                # Convert extracted table to DataFrame
                df = pd.DataFrame(table[0:], columns=headers) if headers else pd.DataFrame(table[0:])
               
                # Replace newlines in text fields
                df = df.map(lambda x: x.replace("\n", " ") if isinstance(x, str) else x)
                # Fill missing values with empty strings
                df.fillna("", inplace=True)  # Fill missing values
                # Define the output CSV filename based on the page number
                csv_filename = os.path.join(output_dir, f"extracted_page_{page_num}.csv")
                 # Save the DataFrame to a CSV file without headers or index
                df.to_csv(csv_filename, index=False, header=False)  # Save without headers

                print(f"Page {page_num} table saveds as {csv_filename}")

# Execute the function to extract tables and save CSVs
extract_tables_per_page(pdf_path, output_dir)


