SELECT 
    COUNT(*) as numbers_of_sales,
    SUM(product_quantity) as product_quantity_count,
    CASE 
        WHEN store_code LIKE 'WEB-%' THEN 'Web'
        ELSE 'Offline'
    END as location
FROM 
    orders_table
GROUP BY 
    location;

