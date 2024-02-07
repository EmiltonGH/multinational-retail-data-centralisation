ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(30),  
    ALTER COLUMN expiry_date TYPE VARCHAR(15),    
    ALTER COLUMN date_payment_confirmed TYPE DATE;