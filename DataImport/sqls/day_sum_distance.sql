SELECT CONVERT(DATE, end_time) AS run_date, joy_run_id, name, SUM(distance) AS distance
FROM run_data
GROUP BY CONVERT(DATE, end_time), joy_run_id, name

