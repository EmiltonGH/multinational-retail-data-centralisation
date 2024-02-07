-- Merges lat and latitude columns as one column latitude
UPDATE dim_store_details
SET latitude = COALESCE(lat, latitude);
ALTER TABLE dim_store_details
DROP COLUMN lat;

-- Update the data types for the dim_store_details
ALTER TABLE dim_store_details
ALTER COLUMN locality TYPE VARCHAR(255),
ALTER COLUMN store_code TYPE VARCHAR(20),
ALTER COLUMN opening_date TYPE DATE,
ALTER COLUMN store_type TYPE VARCHAR(255),
ALTER COLUMN country_code TYPE VARCHAR(20),
ALTER COLUMN continent TYPE VARCHAR(255),
ALTER COLUMN staff_numbers TYPE smallint USING 
  CASE 
    WHEN staff_numbers = 'N/A' OR staff_numbers = 'NULL' THEN NULL 
    WHEN staff_numbers ~ E'^\\d+$' THEN CAST(staff_numbers AS smallint)
    ELSE NULL  
  END,
ALTER COLUMN longitude TYPE FLOAT USING 
  CASE 
    WHEN longitude = 'N/A' OR longitude = 'NULL' THEN NULL 
    WHEN longitude ~ E'^[+-]?([0-9]+\\.?[0-9]*|[0-9]*\\.?[0-9]+)$' THEN CAST(longitude AS FLOAT) 
    ELSE NULL 
  END,
ALTER COLUMN latitude TYPE FLOAT USING 
  CASE 
    WHEN latitude = 'N/A' OR latitude = 'NULL' THEN NULL 
    WHEN latitude ~ E'^[+-]?([0-9]+\\.?[0-9]*|[0-9]*\\.?[0-9]+)$' THEN CAST(latitude AS FLOAT) 
    ELSE NULL 
  END;

--Changes the value from null to N/A
UPDATE dim_store_details
SET locality = 'N/A'
WHERE locality IS NULL;

