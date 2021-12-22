SELECT
    joy_run_id,
    name,
    sum(run_time) AS time
FROM
    run_data
GROUP BY
    joy_run_id,
    name
ORDER BY
    time DESC