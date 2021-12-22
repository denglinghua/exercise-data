SELECT
    joy_run_id,
    name,
    pace
FROM
    (
        SELECT
            joy_run_id,
            name,
            AVG(avg_pace) AS pace,
            sum(distance) AS distance
        FROM
            run_data
        GROUP BY
            joy_run_id,
            name
    ) AS T
WHERE
    T.distance > 3000
ORDER BY
    pace