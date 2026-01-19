from .db import connect
from .logging_utils import get_logger

log = get_logger("transform")

def run():
    conn = connect()
    conn.execute("DELETE FROM station_hourly_join")

    q = '''
    INSERT OR REPLACE INTO station_hourly_join
    SELECT r.station_id, m.site_id, r.ts,
           a.aqhi, a.pm25, r.riders
    FROM ridership_hourly r
    JOIN station_site_map m USING (station_id)
    JOIN aq_hourly a ON a.site_id = m.site_id AND a.ts = r.ts;
    '''
    conn.execute(q)
    conn.commit()

    n = conn.execute("SELECT COUNT(*) FROM station_hourly_join").fetchone()[0]
    log.info("Built station_hourly_join with %d rows", n)
    conn.close()
