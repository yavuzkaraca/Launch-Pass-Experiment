from processing import (load_participant_data, remove_practice_trials, get_slowest_reactions,
                        overview_response_percent_table, launch_percent_overall,
                        remove_vp, remove_invalid_responses, launch_percent_by_factor, fix_response_coding,
                        remove_slow_reactions)

from util import save_csv


def main():
    df = load_participant_data("data")
    df = remove_practice_trials(df)
    df = remove_invalid_responses(df)
    df = remove_slow_reactions(df)
    df = fix_response_coding(df)

    slowest = get_slowest_reactions(df)
    save_csv(slowest, "slowest_reactions.csv")  # Exclude vp19?

    overall_launch = launch_percent_overall(df)
    save_csv(overall_launch, "launch_percent_overall.csv")

    percent_table = overview_response_percent_table(df)
    save_csv(percent_table, "overview_response_percent_table.csv")

    direction_table = launch_percent_by_factor(df, "direction")
    save_csv(direction_table, "response_by_direction.csv")

    start_feature_table = launch_percent_by_factor(df, "startFeature")
    save_csv(start_feature_table, "response_by_startFeature.csv")


if __name__ == "__main__":
    main()
