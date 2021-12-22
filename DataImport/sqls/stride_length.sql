SELECT
	joy_run_id,
	name,
	stride_length
FROM
	(
		SELECT
			joy_run_id,
			name,
			avg(stride_length) AS stride_length,
			sum(distance) AS distance
		FROM
			(
				SELECT
					joy_run_id,
					name,
					stride_length,
					distance
				FROM
					run_data
				WHERE
					stride_length > 0
					AND stride_length < 180
			) AS T
		GROUP BY
			joy_run_id,
			name
	) AS T1
WHERE
	T1.distance > 3000
ORDER BY
	stride_length DESC