# Global Spotify Hits Dashboard

## 1. Dataset and decision-maker

**Project:** Global Spotify Hits Dashboard  
**Primary user:** Playlist Programming Manager at a music streaming service or record label.  
**Dataset files:** `data/track_metadata.csv`, `data/audio_features.csv`, and `data/chart_longevity_panel.csv`. The three files are joined by `track_id`.

**Kaggle dataset page:** TODO — add the exact public Kaggle URL before submission. The uploaded ZIP does not contain this URL, so its provenance cannot be independently confirmed from the files alone.

The supplied README describes 1,200 tracks and release dates from January 2018 through June 2026. The data dictionary describes track metadata, audio features, chart rank, weeks on chart, stream counts, and a viral-hit flag. The files have one row per track rather than a weekly history. The supplied documentation does not establish whether the records are real observations or synthetic examples; we will not describe them as verified real Spotify records unless the original Kaggle page confirms that claim.

### Quick EDA findings

- Each of the three CSV files contains 1,200 rows and `track_id`; joins are one-to-one.
- No missing values were found in the supplied columns.
- The release-date range is January 7, 2018 to June 27, 2026.
- In the merged snapshot, median `weeks_on_top_100` is 18; 28.7% of rows have `is_viral_hit = 1`.
- Pop is the largest genre group in this snapshot (318 tracks). Median chart weeks differ by genre, but group sizes are unequal, so small groups should be interpreted cautiously.
- The data is a cross-sectional snapshot, not a weekly time series. The dashboard therefore compares tracks and genres; it does not claim to show week-by-week changes.

Reproduce the EDA with `python eda.py`. It prints shapes, dtypes, missing values, numeric summaries and a genre summary, and creates two exploratory charts.

## 2. Why a dashboard?

### Who looks at it, and how often?
A Playlist Programming Manager reviews it once a week before deciding which genre segments or tracks deserve additional editorial attention. In a production setting, the underlying chart and stream data would refresh daily, while the manager would make the main programming decisions weekly.

### What decision does it support?
"If the Playlist Programming Manager sees a genre with lower median chart longevity or a lower viral-hit rate, they will review the matching tracks and consider whether playlist placement, promotion, or follow-up analysis is warranted."

This dashboard is a decision aid, not a causal model: genre-level differences alone do not prove that playlist placement caused a track to last longer.

### What happens today without it, and what does that cost?
Without a shared view, the manager may manually combine spreadsheets and compare genres by eye. That takes time, makes comparisons less consistent, and can cause promising or underperforming segments to be overlooked. The current dataset does not include a measured estimate of those costs, so we do not invent a dollar figure.

### Why a dashboard rather than an email or one-off report?
The manager revisits the same questions each week and needs to filter by release year and genre while moving from headline metrics to supporting comparisons and individual tracks. A dashboard lets them explore the same snapshot consistently. A weekly email could summarize the numbers, but it is less useful for interactive drill-down.

## 3. What matters on the dashboard?

### Headline metrics (top of page)
1. **Tracks in selection:** shows the size of the currently filtered group.
2. **Median weeks on Top 100:** a robust summary of typical chart longevity, less affected by a few unusually long-running tracks than the mean.
3. **Marked viral hits:** the share of selected tracks with `is_viral_hit = 1`.

### Supporting charts
1. **Median weeks on Top 100 by genre:** helps compare typical chart longevity across genres.
2. **Share marked as viral by genre:** helps identify genres with a higher proportion of tracks carrying the supplied viral label.

Both charts use the selected release-year range and minimum-weeks threshold, and compare genres side by side. The genre multi-select filters the headline metrics and detail table.

### Filters
- **Release-year range:** compares release cohorts relevant to the manager's review.
- **Genres:** narrows headline metrics and the track-level details to the genres of interest.
- **Minimum weeks on Top 100:** lets the manager focus on tracks with a chosen minimum amount of chart persistence.

### Two things deliberately left out
1. **A chart for every audio feature** (tempo, energy, valence, acousticness, liveness, and danceability). These may be interesting for research, but the dashboard's immediate decision is about chart longevity and genre-level programming review. Adding them would compete with the primary comparisons; they can be explored in a separate analysis.
2. **A release-date trend line presented as chart performance over time.** The data has release dates but no weekly observation date or repeated track-level history. Plotting release year against chart performance would compare release cohorts, not show changes in performance over time, so the dashboard does not present it as a time series.

### Data caveats and safeguards
- The supplied `is_viral_hit` field is treated as an existing label; its definition and derivation need confirmation from the original Kaggle page.
- `peak_chart_rank` uses 1 as the best rank. The detail table states this explicitly to avoid reversing the meaning.
- Genre group sizes vary (for example, Pop has 318 tracks while K-Pop has 59). Compare rates alongside group counts and avoid overinterpreting small groups.
- The supplied files have no missing values, but the production pipeline should continue checking for missing values, duplicate IDs, and schema changes on each refresh.
- The CSV snapshot is static. The page states its release-date coverage and the intended production refresh frequency.

### Page order
1. Title and one-line audience/decision caption.
2. Three headline metrics, visible immediately.
3. Chart-longevity comparison, followed by viral-hit comparison.
4. Expandable track-level table for users who need to investigate individual records.
5. Data caveat at the bottom.

The order prioritizes a quick status check, then the two comparisons that may explain differences, and finally details.

## 4. Refresh frequency and action threshold

### Production refresh and review
- **Intended data refresh:** daily, using the streaming/chart source after confirming a permitted and reliable data feed.
- **Manager review:** weekly, before playlist planning.
- **Why not real time?** The intended decision is weekly programming review; daily refresh is frequent enough to catch meaningful movement without implying that a minute-by-minute change should drive editorial decisions. A production implementation should revisit this choice if the manager begins making same-day placements.
- **Current limitation:** the provided Kaggle files are a frozen snapshot. The deployed app does not fetch new Spotify data automatically.

### What should trigger action?
A practical initial review rule is: **if a genre's median weeks on the Top 100 falls by 20% or more compared with its own prior four-week production baseline, ask the playlist team to investigate that genre's current track mix and placement.** This is a proposed operational threshold, not something that can be calculated from this snapshot, because the supplied data lacks weekly history. Before using it operationally, validate it against real historical data and normal variation.

### What does stale data cost?
A one-day delay may hide a newly emerging or rapidly declining track until the next review. A week-old snapshot may lead the manager to make placement decisions using outdated performance. The impact cannot be quantified from the supplied data alone. The production system should display the latest successful refresh timestamp and alert the data owner if a scheduled refresh fails.

## 5. Run locally

This project uses Streamlit, Pandas, and Plotly.

```bash
uv sync
uv run streamlit run app.py
```

If you are not using `uv`, install the dependencies with:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## 6. GitHub and Streamlit Cloud deployment checklist

1. Create a **public** GitHub repository under your own account.
2. Upload this project's files, including `app.py`, `data/`, `README.md`, `pyproject.toml`, `uv.lock` (if generated), `.python-version`, and `requirements.txt`.
3. Confirm and insert the exact Kaggle dataset page URL in this README.
4. In Streamlit Community Cloud, create an app from the repository and select `app.py` as the entry point.
5. Under **Advanced settings**, choose **Python 3.14**, as required by the assignment.
6. Deploy, open the public app URL, and test the year selector, genre filter, minimum-weeks slider, charts, and detail table.
7. Submit both the deployed app URL and the public GitHub repository URL individually on Canvas.

## Dataset source note

The original Kaggle page URL was not included in the uploaded ZIP. Add it before submission and verify its author, collection method, date coverage, license, and whether the data is real or synthetic. Do not submit an unverified provenance claim.
