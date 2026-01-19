import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from .db import connect
from .config import CFG
from .logging_utils import get_logger

log = get_logger("visualize")

def station_timeline(station_id: str, df: pd.DataFrame, outdir: Path):
    d = df[df["station_id"] == station_id].copy().sort_values("ts")
    if d.empty:
        return

    ci_low = d["mu"] - 1.96*(d["sigma"] / np.sqrt(d["n"].clip(lower=1)))
    ci_high = d["mu"] + 1.96*(d["sigma"] / np.sqrt(d["n"].clip(lower=1)))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d["ts"], y=d["aqhi"], name="AQHI", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=d["ts"], y=ci_low, name="Baseline 95% Low", mode="lines", line=dict(dash="dot")))
    fig.add_trace(go.Scatter(x=d["ts"], y=ci_high, name="Baseline 95% High", mode="lines", line=dict(dash="dot")))

    an = d[d["anomaly"] == 1]
    fig.add_trace(go.Scatter(x=an["ts"], y=an["aqhi"], name="Anomaly", mode="markers",
                             marker=dict(symbol="x", size=10)))

    fig.update_layout(title=f"AQHI & Anomalies — {station_id}", xaxis_title="Time", yaxis_title="AQHI")
    fig.write_html(outdir / f"{station_id}_timeline.html")

def run():
    conn = connect()
    df = pd.read_sql_query("SELECT * FROM exposure_scores", conn, parse_dates=["ts"])
    conn.close()
    if df.empty:
        log.warning("exposure_scores empty; skipping visualization")
        return

    plots_dir = Path(CFG["report_dir"]) / "plots"; plots_dir.mkdir(parents=True, exist_ok=True)
    for sid in sorted(df["station_id"].unique()):
        station_timeline(sid, df, plots_dir)

    summary = (
        df.groupby(["station_id", "hour_of_week"])
          .agg(mean_exposure=("exposure", "mean"),
               anomaly_rate=("anomaly", "mean"),
               obs=("anomaly", "count"))
          .reset_index()
          .sort_values(["mean_exposure", "anomaly_rate"], ascending=[False, False])
    )

    tables_dir = Path(CFG["report_dir"]) / "tables"; tables_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(tables_dir / "top_risky_windows.csv", index=False)
    log.info("Wrote %d station timelines + summary table", df["station_id"].nunique())
