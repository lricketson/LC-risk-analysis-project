import pandas as pd
import numpy as np
import re

PERCENTAGE_CONSTANT = 100
NAN_CUTOFF = 0.95
AVG_CONSTANT = 2
KEPT_COLUMNS = [
    "loan_amnt",
    "term",
    "int_rate",
    "installment",
    "grade",
    "annual_inc",
    "dti",
    "verification_status",
    "avg_fico",
    "earliest_cr_line",
    "total_acc",
    "open_acc",
    "delinq_2yrs",
    "inq_last_6mths",
    "pub_rec",
    "revol_util",
    "revol_bal",
    "home_ownership",
    "did_default",
]


def drop_cols_w_too_many_nans(df: pd.DataFrame):
    too_many_nans_cols = []
    for col in df.columns:
        number_of_nans = df[col].isna().sum()
        col_length = len(df)
        ratio_of_nans = number_of_nans / col_length
        if ratio_of_nans >= NAN_CUTOFF:
            too_many_nans_cols.append(col)
    col_dropped_df = df.drop(columns=too_many_nans_cols)
    return col_dropped_df


def drop_unresolved_loans(df: pd.DataFrame):
    relevant_statuses_list = ["Fully Paid", "Charged Off"]
    filtered_df = df[df["loan_status"].isin(relevant_statuses_list)].copy()
    return filtered_df


def flag_defaults(df: pd.DataFrame):  # to be used after unresolved loans are dropped
    df.loc[:, "did_default"] = df["loan_status"] == "Charged Off"
    return df


def standardise_fico(df: pd.DataFrame):
    df.loc[:, "avg_fico"] = (
        df["fico_range_low"] + df["fico_range_high"]
    ) / AVG_CONSTANT
    return df


def cr_date_to_acc_age(df: pd.DataFrame):
    df.loc[:, "account_age"] = df["earliest_cr_line"]
    return df


def keep_select_cols(df: pd.DataFrame):
    kept_df = df.drop(columns=[col for col in df.columns if col not in KEPT_COLUMNS])
    return kept_df


def preprocess_20col_version(df: pd.DataFrame):
    filtered_df = drop_cols_w_too_many_nans(df)
    filtered_df = standardise_fico(filtered_df)
    filtered_df = drop_unresolved_loans(filtered_df)
    filtered_df = flag_defaults(filtered_df)
    kept_df = keep_select_cols(filtered_df)
    return kept_df


# next job is to collapse some columns down to one by some formula that takes in a bunch of numerical info about them
# and outputs one number, so we can simplify the data hopefully without losing information


# +------------------+ Legacy +------------------+


def further_clean(df: pd.DataFrame):
    inessential_cols_list = [
        "emp_title",
        "url",
        "zip_code",
        "disbursement_method",
        "pymnt_plan",
        "title",
        "id",
        "funded_amnt_inv",
        "funded_amnt",  # we'll use loan_amt instead cos theyre similar
        "installment",
        "loan_status",
        "total_pymnt",
        "total_rec_prncp",
        "total_rec_int",
        "last_pymnt_d",
        "next_pymnt_d",
        "recoveries",
        "collection_recovery_fee",
        "sub_grade",
        "hardship_flag",
        "debt_settlement_flag",
    ]
    cleaned_df = df.drop(columns=inessential_cols_list)
    cleaned_df.loc[:, "avg_fico"] = (
        cleaned_df["fico_range_low"] + cleaned_df["fico_range_high"]
    ) / AVG_CONSTANT
    cleaned_df = cleaned_df.drop(columns=["fico_range_low", "fico_range_high"])
    cleaned_df.loc[:, "term"] = (
        cleaned_df["term"]
        .str.replace(r"(\d+)\s*months?", r"\1", regex=True)
        .astype(int)
    )
    v_map = {"Not Verified": 0, "Verified": 1, "Source Verified": 2}
    cleaned_df.loc[:, "verification_status"] = cleaned_df["verification_status"].map(
        v_map
    )
    grade_map = {g: i + 1 for i, g in enumerate("ABCDEFG")}
    cleaned_df.loc[:, "grade"] = cleaned_df["grade"].map(grade_map)
    # more stuff

    return cleaned_df


def clean_lc_df(df: pd.DataFrame):

    flagged_df = flag_defaults(dropped_df)
    cleaned_df = further_clean(flagged_df)
    return cleaned_df
