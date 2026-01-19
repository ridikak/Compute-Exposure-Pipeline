PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS aq_hourly (
  site_id TEXT NOT NULL,
  ts      TEXT NOT NULL,
  aqhi    REAL,
  pm25    REAL,
  PRIMARY KEY (site_id, ts)
);

CREATE TABLE IF NOT EXISTS ridership_hourly (
  station_id TEXT NOT NULL,
  ts         TEXT NOT NULL,
  riders     INTEGER,
  PRIMARY KEY (station_id, ts)
);

CREATE TABLE IF NOT EXISTS station_site_map (
  station_id TEXT NOT NULL,
  site_id    TEXT NOT NULL,
  distance_m REAL,
  PRIMARY KEY (station_id, site_id)
);

CREATE TABLE IF NOT EXISTS station_hourly_join (
  station_id TEXT, site_id TEXT, ts TEXT,
  aqhi REAL, pm25 REAL, riders INTEGER,
  PRIMARY KEY (station_id, ts)
);

CREATE TABLE IF NOT EXISTS baselines (
  station_id TEXT, hour_of_week INTEGER,
  mu REAL, sigma REAL, n INTEGER,
  PRIMARY KEY (station_id, hour_of_week)
);

CREATE TABLE IF NOT EXISTS exposure_scores (
  station_id TEXT, site_id TEXT, ts TEXT,
  aqhi REAL, riders INTEGER,
  hour_of_week INTEGER,
  mu REAL, sigma REAL, n INTEGER,
  z REAL, anomaly INTEGER,
  exposure REAL,
  PRIMARY KEY (station_id, ts)
);
