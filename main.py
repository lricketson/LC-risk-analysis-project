import pandas as pd
import numpy as np
import re

PERCENTAGE_CONSTANT = 100
NAN_CUTOFF = 0.95
KEPT_COLUMNS = [
    "loan_amnt",
    "term",
    "int_rate",
    "installment",
    "grade",
    "annual_inc",
    "dti",
    "verification_status",
    "earliest_cr_line",
    "total_acc",
    "open_acc",
    "delinq_2yrs",
    "inq_last_6mths",
    "pub_rec",
    "revol_util",
    "revol_bal",
    "home_ownership",
    "fico_range_low",
    "fico_range_high",
    "loan_status",
    "issue_d",
]

SPECIALTY_KEPT_COLUMNS = [
    "loan_amnt",
    "term",
    "int_rate",
    "installment",
    "grade",
    "annual_inc",
    "dti",
    "verification_status",
    "earliest_cr_line",
    "total_acc",
    "open_acc",
    "delinq_2yrs",
    "inq_last_6mths",
    "pub_rec",
    "revol_util",
    "revol_bal",
    "home_ownership",
    "fico_range_low",
    "fico_range_high",
    "loan_status",
    "issue_d",
]


def drop_cols_w_too_many_nans(df: pd.DataFrame):
    """
    Drops columns which are at least 95% NaNs.
    """
    too_many_nans_cols = []
    for col in df.columns:
        number_of_nans = df[col].isna().sum()
        col_length = len(df)
        ratio_of_nans = number_of_nans / col_length
        if ratio_of_nans >= NAN_CUTOFF:
            too_many_nans_cols.append(col)
    col_dropped_df = df.drop(columns=too_many_nans_cols)
    return col_dropped_df


def filter_and_label_defaults(df: pd.DataFrame):
    """
    Drops all unresolved loans, and creates a new column which labels whether a borrower
    defaulted or not.
    """
    relevant_statuses_list = ["Fully Paid", "Charged Off"]
    df = df[df["loan_status"].isin(relevant_statuses_list)].copy()
    df.loc[:, "did_default"] = df["loan_status"] == "Charged Off"
    df = df.drop(columns="loan_status")
    return df


def add_avg_fico_col(df: pd.DataFrame):
    """
    Finds the average of the highest and lowest FICO scores of the borrower for simplicity.
    """
    df.loc[:, "avg_fico"] = (df["fico_range_low"] + df["fico_range_high"]) / 2
    df = df.drop(columns=["fico_range_low", "fico_range_high"])
    return df


def convert_cr_date_to_acc_age(df: pd.DataFrame):
    """
    Finds age of credit account by finding the number of years between loan request
    and earliest credit line. Creates a new column for age of account in years.
    """
    df["earliest_cr_line"] = pd.to_datetime(
        df["earliest_cr_line"],
        format="%b-%Y",
        errors="coerce",
    )
    df["issue_d"] = pd.to_datetime(df["issue_d"], format="%b-%Y", errors="coerce")
    df["credit_age_yrs"] = (
        (df["issue_d"] - df["earliest_cr_line"]).dt.days / 365.25
    ).round(2)
    df = df.drop(columns=["earliest_cr_line", "issue_d"])
    return df


def encode_verification_status(df: pd.DataFrame):
    """
    Ordinally encodes verification status of a borrower's income, on a
    scale of 0 (least good) to 2 (most good).
    """
    v_map = {"Not Verified": 0, "Verified": 1, "Source Verified": 2}
    df.loc[:, "verification_status"] = df["verification_status"].map(v_map)
    return df


def encode_grade(df: pd.DataFrame):
    """
    Replaces grades from A-G with grades from 0-6. A = 0, B = 1, ..., G = 6.
    """
    grade_map = {g: i for i, g in enumerate("ABCDEFG")}
    df.loc[:, "grade"] = df["grade"].map(grade_map)
    return df


def encode_term(df: pd.DataFrame):
    """
    Replaces "n months" with just n as an integer.
    """
    df.loc[:, "term"] = (
        df["term"].str.replace(r"(\d+)\s*months?", r"\1", regex=True).astype(int)
    )
    return df


def encode_home_ownership(df: pd.DataFrame):
    """
    Encodes home ownership ordinally on a scale of 0 (least good) to 2 (most good).
    """
    home_ownership_map = {"RENT": 0, "MORTGAGE": 1, "OWN": 2}
    df.loc[:, "home_ownership"] = df["home_ownership"].map(home_ownership_map)
    return df


def keep_select_cols(df: pd.DataFrame):
    """
    Keeps selected columns and discards the rest.
    """
    return df[KEPT_COLUMNS]


def test_pd(df: pd.DataFrame):
    mykeptcols = ["loan_amnt", "grade", "term"]
    mydf = df[mykeptcols]
    return mydf


def preprocess_df(df: pd.DataFrame):
    df = keep_select_cols(df)
    df = drop_cols_w_too_many_nans(df)
    df = filter_and_label_defaults(df)
    df = add_avg_fico_col(df)
    df = convert_cr_date_to_acc_age(df)
    df = encode_verification_status(df)
    df = encode_grade(df)
    df = encode_term(df)
    df = encode_home_ownership(df)
    return df


def count_nans_in_column(col: pd.Series):
    return col.isna().sum()


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
