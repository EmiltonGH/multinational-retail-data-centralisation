DELETE FROM dim_card_details
WHERE card_number IN (
    SELECT card_number
    FROM dim_card_details
    GROUP BY card_number
    HAVING COUNT(*) > 1
);

