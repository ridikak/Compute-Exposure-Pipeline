import numpy as np
import pandas as pd
from pathlib import Path
from .db import connect
from .config import CFG
from .logging_utils import get_logger

log = get_logger("anomalies")

def run():
    conn = connect()
    eps = float(CFG["epsilon"])
    thr = float(CFG["anomaly_threshold"])

    df = pd.read_sql_query("SELECT station_id, site_id, ts, aqhi, riders FROM station_hourly_join",
                           conn, parse_dates=["ts"])
    if df.empty:
        log.warning("station_hourly_join empty; skipping anomalies")
        conn.close()
        return

    df["hour_of_week"] = df["ts"].dt.dayofweek*24 + df["ts"].dt.hour
    base = pd.read_sql_query("SELECT * FROM baselines", conn)

    out = df.merge(base, on=["station_id", "hour_of_week"], how="left")
    out["sigma"] = out["sigma"].fillna(0.0)
    out["mu"] = out["mu"].fillna(out["aqhi"].mean())
    out["n"] = out["n"].fillna(1).astype(int)

    denom = out["sigma"].replace(0, np.nan) + eps
    out["z"] = (out["aqhi"] - out["mu"]) / denom
    out["z"] = out["z"].fillna(0.0)
    out["anomaly"] = (out["z"].abs() >= thr).astype(int)

    out["riders"] = out["riders"].fillna(0).astype(int)
    out["exposure"] = out["aqhi"] * out["riders"].clip(lower=0)

    cols = ["station_id","site_id","ts","aqhi","riders","hour_of_week","mu","sigma","n","z","anomaly","exposure"]

    conn.execute("DELETE FROM exposure_scores")
    out[cols].to_sql("exposure_scores", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()

    out_dir = Path(CFG["output_dir"]); out_dir.mkdir(parents=True, exist_ok=True)
    out[cols].to_parquet(out_dir / "exposure_scores.parquet", index=False)
    log.info("Wrote exposure_scores: %d rows (SQLite + Parquet)", len(out))
