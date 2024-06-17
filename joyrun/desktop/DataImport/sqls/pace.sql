SELECT joy_run_id, name, SUM(run_time) / SUM(distance) AS pace, SUM(distance) AS distance
FROM regular_run_view
GROUP BY joy_run_id, name
HAVING SUM(distance) > 1500
ORDER BY pace