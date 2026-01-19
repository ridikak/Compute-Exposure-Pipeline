import pandas as pd
from pathlib import Path
from .db import connect
from .config import CFG
from .logging_utils import get_logger

log = get_logger("features")

def run():
    conn = connect()
    df = pd.read_sql_query("SELECT station_id, ts, aqhi FROM station_hourly_join", conn, parse_dates=["ts"])
    if df.empty:
        log.warning("station_hourly_join empty; skipping features")
        conn.close()
        return

    df["hour_of_week"] = df["ts"].dt.dayofweek*24 + df["ts"].dt.hour

    baselines = (
        df.groupby(["station_id", "hour_of_week"])["aqhi"]
          .agg(mu="mean", sigma=lambda x: x.std(ddof=1), n="count")
          .reset_index()
    )
    baselines["sigma"] = baselines["sigma"].fillna(0.0)

    conn.execute("DELETE FROM baselines")
    baselines.to_sql("baselines", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()

    out_dir = Path(CFG["output_dir"]); out_dir.mkdir(parents=True, exist_ok=True)
    baselines.to_parquet(out_dir / "baselines.parquet", index=False)
    log.info("Wrote baselines: %d rows (SQLite + Parquet)", len(baselines))
