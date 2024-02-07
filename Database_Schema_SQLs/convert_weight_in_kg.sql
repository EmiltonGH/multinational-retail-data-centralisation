UPDATE dim_products
SET weight = 
    CASE
        WHEN weight LIKE '%kg%' THEN
            ROUND(CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS DECIMAL(10, 3)), 3)
        WHEN weight LIKE '%g%' THEN
            ROUND(CAST(REGEXP_REPLACE(weight, '[^0-9.]', '', 'g') AS DECIMAL(10, 3)) / 1000, 3)
        WHEN weight LIKE '%x%' THEN
            ROUND(
                CAST(REGEXP_REPLACE(SPLIT_PART(weight, 'x', 1), '[^0-9.]', '', 'g') AS DECIMAL(10, 3))
                * CAST(REGEXP_REPLACE(SPLIT_PART(weight, 'x', 2), '[^0-9.]', '', 'g') AS DECIMAL(10, 3)),
                3
            )
        ELSE
            NULL
    END;
