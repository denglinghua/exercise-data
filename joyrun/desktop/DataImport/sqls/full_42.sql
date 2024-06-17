SELECT joy_run_id, name, COUNT(*) AS full_marathon
FROM run_data
WHERE distance > 42
GROUP BY joy_run_id, name
ORDER BY full_marathon DESC