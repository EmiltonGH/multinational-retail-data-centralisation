-- Change product_price from TEXT to FLOAT
ALTER TABLE dim_products
ALTER COLUMN product_price TYPE FLOAT USING NULLIF(product_price, '')::FLOAT;

-- Change weight from TEXT to FLOAT
ALTER TABLE dim_products
ALTER COLUMN weight TYPE FLOAT USING NULLIF(weight, '')::FLOAT;

-- Change EAN from TEXT to VARCHAR
ALTER TABLE dim_products
ALTER COLUMN "EAN" TYPE VARCHAR(20); 

-- Change product_code from TEXT to VARCHAR
ALTER TABLE dim_products
ALTER COLUMN product_code TYPE VARCHAR(20); 

-- Change date_added from TEXT to DATE
ALTER TABLE dim_products
ALTER COLUMN date_added TYPE DATE USING date_added::DATE;

-- Change uuid from TEXT to UUID
ALTER TABLE dim_products
ALTER COLUMN uuid TYPE UUID USING uuid::UUID;

-- Change still_available from TEXT to BOOL
ALTER TABLE dim_products
ALTER COLUMN still_available TYPE BOOL USING CASE WHEN still_available = 'true' THEN true ELSE false END;

-- Change weight_class datatype from TEXT to VARCHAR
ALTER TABLE dim_products
ALTER COLUMN weight_class TYPE VARCHAR(30); 