import pandas as pd
from .config import CFG
from .db import connect
from .utils import make_synthetic
from .logging_utils import get_logger

log = get_logger("extract")

def ensure_tables(conn):
    conn.executescript(open("sql/01_create_tables.sql").read())
    conn.executescript(open("sql/02_indexes.sql").read())

def load_df(conn, df: pd.DataFrame, table: str):
    df = df.copy()
    if "ts" in df.columns:
        df["ts"] = pd.to_datetime(df["ts"]).dt.floor("H").astype(str)
    df.to_sql(table, conn, if_exists="append", index=False)

def run(use_synthetic: bool = True):
    conn = connect()
    ensure_tables(conn)

    if use_synthetic:
        aq, rid, mapping = make_synthetic()
        log.info("Using synthetic data: aq=%d, ridership=%d, mapping=%d", len(aq), len(rid), len(mapping))
    else:
        aq = pd.read_csv(CFG["aq_csv"])
        rid = pd.read_csv(CFG["ridership_csv"])
        mapping = pd.read_csv(CFG["map_csv"])
        log.info("Loaded CSVs: aq=%d, ridership=%d, mapping=%d", len(aq), len(rid), len(mapping))

    conn.execute("DELETE FROM aq_hourly")
    conn.execute("DELETE FROM ridership_hourly")
    conn.execute("DELETE FROM station_site_map")

    load_df(conn, aq, "aq_hourly")
    load_df(conn, rid, "ridership_hourly")
    load_df(conn, mapping, "station_site_map")

    conn.commit()
    conn.close()
