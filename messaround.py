import pandas as pd

df = pd.read_csv(
    "./datasets/lc_data_2007_to_2018.csv",
    low_memory=False,
    encoding="latin1",
    nrows=100000,  # only looking at 100k rows right now for performance
)
pd.set_option("display.max_columns", 170)


print(df.columns)
