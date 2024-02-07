SELECT
    SUM(staff_numbers) AS total_staff_numbers,
    SUBSTRING(country_code, 1, 2) AS country_code
FROM
    dim_store_details
WHERE
    LENGTH(country_code) = 2
GROUP BY
    country_code;
