SELECT joy_run_id, name, C.month_no AS year_month,
	SUM(run_time) / SUM(distance) AS avg_pace
FROM regular_run_view AS R INNER JOIN run_calendar AS C
	ON CONVERT(DATE, R.end_time) = C.day
GROUP BY joy_run_id, name, C.month_no