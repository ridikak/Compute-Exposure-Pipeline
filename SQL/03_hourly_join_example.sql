WITH ridership_hourly_aligned AS (
  SELECT station_id, substr(ts, 1, 13) || ':00:00' AS ts_hour, CAST(riders AS INTEGER) AS riders
  FROM ridership_hourly
),
aq_hourly_aligned AS (
  SELECT site_id, substr(ts, 1, 13) || ':00:00' AS ts_hour, CAST(aqhi AS REAL) AS aqhi, CAST(pm25 AS REAL) AS pm25
  FROM aq_hourly
)
INSERT OR REPLACE INTO station_hourly_join (station_id, site_id, ts, aqhi, pm25, riders)
SELECT r.station_id, m.site_id, r.ts_hour AS ts, a.aqhi, a.pm25, r.riders
FROM ridership_hourly_aligned r
JOIN station_site_map m USING (station_id)
JOIN aq_hourly_aligned a ON a.site_id = m.site_id AND a.ts_hour = r.ts_hour;
