SELECT
    joy_run_id,
    name,
    count(*) AS times
FROM
    run_data
GROUP BY
    joy_run_id,
    name
ORDER BY
    times DESC