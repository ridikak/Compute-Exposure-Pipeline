CREATE INDEX IF NOT EXISTS idx_join_ts ON station_hourly_join(ts);
CREATE INDEX IF NOT EXISTS idx_baselines_s_h ON baselines(station_id, hour_of_week);
CREATE INDEX IF NOT EXISTS idx_scores_anom ON exposure_scores(anomaly);
