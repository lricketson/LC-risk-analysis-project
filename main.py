import pandas as pd
import numpy as np

PERCENTAGE_CONSTANT = 100
NAN_CUTOFF = 0.95


df = pd.read_csv(
    "./datasets/lc_data_2007_to_2018.csv",
    low_memory=False,
    encoding="latin1",
    nrows=10000,  # only looking at 10k rows right now for performance
)

pd.set_option("display.max_columns", None)

first_row = df.iloc[0]

# print(f"BEFORE: NUMBER OF ROWS IN DF: {len(df.columns)}")


# print(f"Number of NaNs: {first_row.isna().sum()}")


def drop_inessential_data(df: pd.DataFrame):
    inessential_cols_list = ["emp_title", "url", "zip_code"]
    for col in df.columns:
        number_of_nans = df[col].isna().sum()
        col_length = len(df)
        ratio_of_nans = number_of_nans / col_length
        if ratio_of_nans >= NAN_CUTOFF:
            inessential_cols_list.append(col)
    col_dropped_df = df.drop(columns=inessential_cols_list)
    row_dropped_df = col_dropped_df["loan_status" != "Current"]
    return row_dropped_df


def flag_defaults(df: pd.DataFrame):
    df['did_default'] = df['loan_status' == ]

def clean_lc_df(df):
    dropped_df = drop_inessential_data(df)


# next job is to collapse some columns down to one by some formula that takes in a bunch of numerical info about them
# and outputs one number, so we can simplify the data hopefully without losing information


print(df.head())

# print(f"AFTER: NUMBER OF ROWS IN DF: {len(df.columns)}")
