from processing import (load_participant_data, remove_practice_trials, get_slowest_reactions, overview_response_percent_table,
                        remove_vp, remove_invalid_responses, response_percent_by_factor)

from util import save_csv


def main():
    df = load_participant_data("data")
    """
    print(df.shape)  # (9324, 11), which is correct, concat worked as intended
    print(df.head())  # Seems fine
    print(df.columns)  # Seems fine
    print(df.isna().any().any())  # Cool, no missing values
    """

    df = remove_practice_trials(df)
    df = remove_invalid_responses(df)
    # df = remove_vp(df, 21)  # or 21 bc it has different labels?

    slowest = get_slowest_reactions(df)
    save_csv(slowest, "slowest_reactions.csv")  # Exclude vp19?

    percent_table = overview_response_percent_table(df)
    save_csv(percent_table, "overview_response_percent_table.csv")

    direction_table = response_percent_by_factor(df, "direction")
    save_csv(direction_table, "response_by_direction.csv")

    start_feature_table = response_percent_by_factor(df, "startFeature")
    save_csv(start_feature_table, "response_by_startFeature.csv")


if __name__ == "__main__":
    main()
