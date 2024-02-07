UPDATE dim_products
SET weight_class = 
  CASE 
    WHEN CAST(weight AS FLOAT) < 2.0 THEN 'Light'
    WHEN CAST(weight AS FLOAT) >= 2.0 AND CAST(weight AS FLOAT) < 40.0 THEN 'Mid_Sized'
    WHEN CAST(weight AS FLOAT) >= 40.0 AND CAST(weight AS FLOAT) < 140.0 THEN 'Heavy'
    WHEN CAST(weight AS FLOAT) >= 140.0 THEN 'Truck_Required'
    ELSE NULL
  END;
