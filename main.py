import pandas as pd
import numpy as np

PERCENTAGE_CONSTANT = 100

df = pd.read_csv(
    "./datasets/lc_data_2007_to_2018.csv",
    low_memory=False,
    encoding="latin1",
    nrows=10000,  # only looking at 10k rows right now for performance
)

first_row = df.iloc[0]

# print(f"Number of NaNs: {first_row.isna().sum()}")
for col in df.columns:
    number_of_nans = df[col].isna().sum()
    col_length = len(df)
    ratio_of_nans = number_of_nans / col_length
    print(col, round(PERCENTAGE_CONSTANT * ratio_of_nans, 2))


print(f"NUMBER OF ROWS IN DF: {len(df)}")
