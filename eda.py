from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).parent / "data"
meta = pd.read_csv(DATA_DIR / "track_metadata.csv")
audio = pd.read_csv(DATA_DIR / "audio_features.csv")
panel = pd.read_csv(DATA_DIR / "chart_longevity_panel.csv")

print("SHAPES")
print("metadata:", meta.shape, "audio:", audio.shape, "performance:", panel.shape)

for name, data in [
    ("metadata", meta),
    ("audio", audio),
    ("performance", panel),
]:
    print(f"\n{name.upper()} DATA TYPES")
    print(data.dtypes)
    print(f"\n{name.upper()} MISSING VALUES")
    print(data.isna().sum())

df = meta.merge(audio, on="track_id", validate="one_to_one")
df = df.merge(panel, on="track_id", validate="one_to_one")
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df["release_year"] = df["release_date"].dt.year

print("\nMERGED SHAPE:", df.shape)
print("Duplicate track IDs:", df["track_id"].duplicated().sum())
print("Release-date range:", df["release_date"].min(), "to", df["release_date"].max())
print("\nNUMERIC SUMMARY")
print(df.describe(include="number").round(2).T)
print("\nGENRE SUMMARY")
print(
    df.groupby("genre")
    .agg(
        tracks=("track_id", "count"),
        median_weeks=("weeks_on_top_100", "median"),
        median_streams_mil=("total_streams_mil", "median"),
        viral_rate=("is_viral_hit", "mean"),
    )
    .sort_values("median_weeks", ascending=False)
    .round(3)
)

# Chart 1: distribution of chart longevity
plt.figure(figsize=(8, 5))
df["weeks_on_top_100"].hist(bins=20)
plt.title("Distribution of Weeks on Top 100")
plt.xlabel("Weeks")
plt.ylabel("Number of tracks")
plt.tight_layout()
plt.savefig("eda_weeks_distribution.png", dpi=150)
plt.show()

# Chart 2: genre-level median longevity
genre_summary = df.groupby("genre")["weeks_on_top_100"].median().sort_values()
plt.figure(figsize=(9, 5))
genre_summary.plot(kind="barh")
plt.title("Median Weeks on Top 100 by Genre")
plt.xlabel("Median weeks")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig("eda_genre_longevity.png", dpi=150)
plt.show()
