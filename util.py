from pathlib import Path


def save_csv(df, filename, index=True):
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)

    path = out_dir / filename
    df.to_csv(path, index=index)
