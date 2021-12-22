SELECT
	joy_run_id,
	name,
	count(*) AS full_marathon
FROM
	(
		SELECT
			joy_run_id,
			name
		FROM
			run_data
		WHERE
			distance > 42
	) AS T
GROUP BY
	joy_run_id,
	name
ORDER BY
	full_marathon DESC