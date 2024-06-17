SELECT D.joy_run_id, D.name, C.week_no, SUM(D.distance) AS distance
FROM day_distance_view AS D INNER JOIN run_calendar AS C ON D.run_date = C.day
GROUP BY D.joy_run_id, D.name, C.week_no