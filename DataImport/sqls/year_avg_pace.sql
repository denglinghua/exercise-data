SELECT joy_run_id, name, YEAR(end_time) AS year,
	SUM(run_time) / SUM(distance) AS pace
FROM regular_run_view
GROUP BY joy_run_id, name, YEAR(end_time)