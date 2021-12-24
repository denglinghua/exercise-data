SELECT joy_run_id, name, ROUND(SUM(distance), 0) AS distance
FROM run_data
GROUP BY joy_run_id, name
ORDER BY distance DESC