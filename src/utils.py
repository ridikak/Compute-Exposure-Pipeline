import numpy as np
import pandas as pd

def make_synthetic(start="2025-06-01", hours=7*24, stations=5, seed=7):
    rng = np.random.default_rng(seed)
    ts = pd.date_range(start, periods=hours, freq="H")
    station_ids = [f"S{i:02d}" for i in range(stations)]
    site_ids = [f"AQ{i:02d}" for i in range(stations)]

    ridership = []
    for s in station_ids:
        base = 100 + 60*np.sin(2*np.pi*(ts.hour/24)) + 40*(ts.dayofweek < 5)
        r = np.maximum(0, base + rng.normal(0, 15, size=len(ts))).round().astype(int)
        ridership.append(pd.DataFrame({"station_id": s, "ts": ts, "riders": r}))
    ridership = pd.concat(ridership, ignore_index=True)

    aq_list = []
    for site in site_ids:
        base = 3 + 0.8*np.sin(2*np.pi*(ts.hour/24)) + 0.4*(ts.dayofweek >= 5)
        spikes = (rng.random(len(ts)) < 0.03) * rng.normal(3.5, 1.0, len(ts))
        aqhi = np.clip(base + spikes + rng.normal(0, 0.4, len(ts)), 1, 10)
        pm25 = np.clip(5 + 3*np.sin(2*np.pi*(ts.hour/24)) + spikes*2 + rng.normal(0, 1.2, len(ts)), 0, 80)
        aq_list.append(pd.DataFrame({"site_id": site, "ts": ts, "aqhi": aqhi, "pm25": pm25}))
    aq = pd.concat(aq_list, ignore_index=True)

    mapping = pd.DataFrame({
        "station_id": station_ids,
        "site_id": site_ids,
        "distance_m": rng.integers(100, 900, size=stations).astype(float)
    })

    return aq, ridership, mapping
