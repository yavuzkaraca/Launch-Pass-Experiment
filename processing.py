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


def remove_slow_reactions(df, max_rt_ms=6000):
    return df[df["RT"] <= max_rt_ms].copy()


def get_slowest_reactions(df):
    return df.sort_values("RT", ascending=False).head(20)


def remove_vp(df, vp_id):
    return df[df["vp"] != vp_id].copy()


# Some participants understood the buttons differently
_TEAM_PASS_EQUALS_1 = [4, 16, 17, 18, 19, 20, 21]
_TEAM_PASS_EQUALS_2 = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


def fix_response_coding(df):
    mask = df["vp"].isin(_TEAM_PASS_EQUALS_2) & df["response"].isin([1, 2])
    df.loc[mask, "response"] = df.loc[mask, "response"].map({1: 2, 2: 1})
    return df


def launch_percent_overall(df):
    """
    Computes overall Launch percentage (response == 2),
    averaged across participants (mean ± std).
    """

    # per-participant totals
    totals = (
        df.groupby("vp")
        .size()
        .reset_index(name="n_total")
    )

    # per-participant launch counts
    launches = (
        df[df["response"] == 2]
        .groupby("vp")
        .size()
        .reset_index(name="n_launch")
    )

    per_vp = totals.merge(launches, on="vp", how="left")
    per_vp["n_launch"] = per_vp["n_launch"].fillna(0)

    per_vp["launch_percent"] = per_vp["n_launch"] / per_vp["n_total"] * 100

    table = per_vp["launch_percent"].agg(["mean", "std"]).to_frame().T
    table.columns = ["Launch_mean", "Launch_std"]

    return table


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
        .rename(columns={1: "Pass_%", 2: "Launch_%"})
    )

    return table


def launch_percent_by_factor(df, factor):
    """
    Mean ± std of Launch response percentage (response == 2)
    per level of `factor`, computed per participant first.
    """

    # per-vp counts (all responses)
    totals = (
        df.groupby(["vp", factor])
        .size()
        .reset_index(name="n_total")
    )

    # per-vp counts (launch only)
    launches = (
        df[df["response"] == 2]
        .groupby(["vp", factor])
        .size()
        .reset_index(name="n_launch")
    )

    per_vp = totals.merge(launches, on=["vp", factor], how="left")
    per_vp["n_launch"] = per_vp["n_launch"].fillna(0)

    per_vp["launch_percent"] = per_vp["n_launch"] / per_vp["n_total"] * 100

    table = (
        per_vp
        .groupby(factor)["launch_percent"]
        .agg(["mean", "std"])
        .rename(columns={"mean": "Launch_mean", "std": "Launch_std"})
    )

    return table
