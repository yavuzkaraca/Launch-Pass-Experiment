import matplotlib.pyplot as plt


def plot_rt_histogram(df, bins=100):
    plt.hist(df["RT"], bins=bins)
    plt.xlabel("Reaction Time (ms)")
    plt.ylabel("Count")
    plt.title("Distribution of Reaction Times (all participants)")
    plt.show()


def plot_rt_per_participant(df, alpha=0.4, jitter=0.1, cutoff_ms=5000):
    vps = sorted(df["vp"].unique())

    x = []
    y = []

    for i, vp in enumerate(vps):
        rt_values = df.loc[df["vp"] == vp, "RT"]
        x.extend([i] * len(rt_values))
        y.extend(rt_values)

    plt.figure(figsize=(12, 4))
    plt.scatter(x, y, alpha=alpha)

    plt.axhline(cutoff_ms, linestyle="--", linewidth=2, label=f"{cutoff_ms} ms")

    plt.xticks(range(len(vps)), vps)
    plt.xlabel("Participant (vp)")
    plt.ylabel("Reaction Time (ms)")
    plt.title("Reaction Times per Participant")

    plt.show()
