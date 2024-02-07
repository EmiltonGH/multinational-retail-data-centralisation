SELECT
    ROUND(SUM(CAST(ot.product_quantity * p.product_price AS NUMERIC)), 2) AS total_sales,
    dt.year,
    dt.month
FROM
    orders_table ot
JOIN
    dim_date_times dt ON ot.date_uuid = dt.date_uuid
JOIN
    dim_products p ON ot.product_code = p.product_code
GROUP BY
    dt.year,
    dt.month
ORDER BY
    total_sales DESC;
