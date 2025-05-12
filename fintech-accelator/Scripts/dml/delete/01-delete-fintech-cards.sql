-- DELETE last payment method
DELETE FROM fintech.payment_methods
WHERE method_id = (SELECT method_id 
                  FROM fintech.payment_methods
                  WHERE name = 'Apple Pay');