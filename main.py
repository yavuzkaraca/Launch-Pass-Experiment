from processing import load_participant_data, remove_practice_trials


def main():
    df = load_participant_data("data")
    print(df.shape)  # (9324, 11), which is correct, concat worked as intended
    print(df.head())  # Seems fine
    print(df.columns)  # Seems fine
    print(df.isna().any().any())  # Cool, no missing values

    df = remove_practice_trials(df)


if __name__ == "__main__":
    main()
