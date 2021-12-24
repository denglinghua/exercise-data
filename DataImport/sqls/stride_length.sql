SELECT joy_run_id, name, AVG(stride_length) AS stride_length, SUM(distance) AS distance
FROM regular_run_view
WHERE stride_length > 0 AND stride_length < 180
GROUP BY joy_run_id, name
HAVING SUM(distance) > 3000
ORDER BY stride_length DESC