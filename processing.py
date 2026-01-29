import pandas as pd
from pathlib import Path


def load_participant_data(data_dir):
    dfs = []

    for f in Path(data_dir).glob("*.csv"):
        dfs.append(pd.read_csv(f, skipinitialspace=True))

    return pd.concat(dfs, ignore_index=True)


def remove_practice_trials(df):
    return df[df["practice"] == 0].copy()


def remove_invalid_responses(df):
    return df[df["response"].isin([1, 2])].copy()


def get_slowest_reactions(df):
    return df.sort_values("RT", ascending=False).head(20)


def remove_vp(df, vp_id):
    return df[df["vp"] != vp_id].copy()


def overview_response_percent_table(df):
    counts = (
        df
        .groupby(["featureBias", "soundBias", "response"])
        .size()
        .reset_index(name="n")
    )

    counts["percent"] = (
            counts["n"]
            / counts.groupby(["featureBias", "soundBias"])["n"].transform("sum")
            * 100
    )

    table = (
        counts
        .pivot_table(
            index=["featureBias", "soundBias"],
            columns="response",
            values="percent"
        )
        .rename(columns={1: "Launch_%", 2: "Pass_%"})
    )

    return table


def response_percent_by_factor(df, factor):
    per_vp = (
        df
        .groupby(["vp", factor, "response"])
        .size()
        .reset_index(name="n")
    )

    per_vp["percent"] = (
        per_vp["n"]
        / per_vp.groupby(["vp", factor])["n"].transform("sum")
        * 100
    )

    # aggregate across participants
    summary = (
        per_vp
        .groupby([factor, "response"])["percent"]
        .agg(["mean", "std"])
        .reset_index()
    )

    table = (
        summary
        .pivot_table(
            index=factor,
            columns="response",
            values=["mean", "std"]
        )
    )

    # nicer column names
    table.columns = [
        f"{'Pass' if r == 1 else 'Launch'}_{stat}"
        for stat, r in table.columns
    ]

    return table

