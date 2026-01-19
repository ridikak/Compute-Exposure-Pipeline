# Commute Exposure Pipeline (pandas + SQL + NumPy + Plotly)

End-to-end data pipeline that fuses hourly transit ridership and air-quality readings,
computes station×hour baselines (mu, sigma), detects z-score anomalies, and produces
Plotly reports plus ranked tables of high-risk commute windows.

## Highlights
- ETL into SQLite (raw tables) -> hourly join fact table
- Baseline stats per station × hour-of-week: mean (mu), std dev (sigma), count (n)
- Z-score anomaly detection and ridership-weighted exposure index (AQHI × riders)
- Outputs persisted to SQLite + Parquet checkpoints + Plotly HTML reports
- Synthetic data generator for instant demo + basic tests

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.main --synthetic
```

Stage-by-stage:
```bash
python -m src.main --stage extract --synthetic
python -m src.main --stage transform
python -m src.main --stage features
python -m src.main --stage anomalies
python -m src.main --stage visualize
```

## Outputs
- SQLite tables: `station_hourly_join`, `baselines`, `exposure_scores`
- Parquet checkpoints: `data/processed/baselines.parquet`, `data/processed/exposure_scores.parquet`
- Plotly HTML timelines: `reports/plots/*_timeline.html`
- Summary CSV: `reports/tables/top_risky_windows.csv`
