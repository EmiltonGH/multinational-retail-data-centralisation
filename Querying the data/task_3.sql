SELECT
    CAST(SUM(p.product_price * o.product_quantity) AS numeric(10, 2)) AS total_sales,
    dt.month AS month
FROM
    dim_products p
JOIN
    orders_table o ON p.product_code = o.product_code
JOIN
    dim_date_times dt ON o.date_uuid = dt.date_uuid
GROUP BY
    dt.month
ORDER BY
    total_sales DESC;
