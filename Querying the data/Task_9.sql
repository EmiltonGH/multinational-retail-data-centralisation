WITH sales_time_gaps AS (
  SELECT 
    year,
    EXTRACT(EPOCH FROM lead_ts - timestamp) * 1000 AS time_difference_ms
  FROM (
    SELECT 
      year,
      TO_TIMESTAMP(timestamp, 'HH24:MI:SS') AS timestamp,
      LEAD(TO_TIMESTAMP(timestamp, 'HH24:MI:SS')) OVER (PARTITION BY year ORDER BY timestamp) AS lead_ts
    FROM dim_date_times
  ) AS time_components
)

SELECT 
  year,
  CONCAT(
    '"hours": ', FLOOR(AVG(time_difference_ms) / (3600 * 1000)),
    ', "minutes": ', FLOOR((AVG(time_difference_ms) % (3600 * 1000)) / (60 * 1000)),
    ', "seconds": ', FLOOR((AVG(time_difference_ms) % (60 * 1000)) / 1000),
    ', "milliseconds": ', FLOOR(AVG(time_difference_ms) % 1000)
  ) AS actual_time_taken
FROM sales_time_gaps
GROUP BY year;
