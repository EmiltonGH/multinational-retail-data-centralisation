SELECT
    d.store_type,
    CAST(SUM(o.product_quantity * p.product_price) AS NUMERIC(10, 2)) AS total_sales,
    CAST((SUM(o.product_quantity * p.product_price) / 
          (SELECT SUM(o2.product_quantity * p2.product_price) 
           FROM orders_table o2
           JOIN dim_products p2 ON o2.product_code = p2.product_code)) * 100 AS NUMERIC(5, 2)) AS percentage_total
FROM
    dim_store_details d
JOIN
    orders_table o ON d.store_code = o.store_code
JOIN
    dim_products p ON o.product_code = p.product_code
GROUP BY
    d.store_type
ORDER BY
    total_sales DESC;
