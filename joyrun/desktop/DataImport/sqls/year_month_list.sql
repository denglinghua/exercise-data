SELECT CAST(years.n AS VARCHAR(4)) + '-' + RIGHT('00' + CAST(months.n AS VARCHAR(2)), 2) AS year_month
FROM (VALUES(2019),(2020),(2021)) years(n),
     (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) months(n)
 ORDER BY 1