import pandas as pd
from pathlib import Path


def load_participant_data(data_dir):
    dfs = []

    for f in Path(data_dir).glob("*.csv"):
        dfs.append(pd.read_csv(f, skipinitialspace=True))

    return pd.concat(dfs, ignore_index=True)


def remove_practice_trials(df):
    return df[df["practice"] == 0].copy()
