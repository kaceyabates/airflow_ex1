import pandas as pd
import glob

def run_query(input_dir):
    # Load both CSVs from the final directory
    files = glob.glob(f"{input_dir}/*.csv")

    dfs = [pd.read_csv(f, header=None) for f in files]

    # Example query: print the number of rows for each symbol
    for f, df in zip(files, dfs):
        print(f"File: {f}, Rows: {len(df)}")
