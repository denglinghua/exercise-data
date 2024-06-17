SELECT joy_run_id, name, COUNT(*) AS run_times
FROM day_distance_view
GROUP BY joy_run_id, name
ORDER BY run_times DESC