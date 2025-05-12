-- update fintech.issuers
-- SELECT name issuers
SELECT issuer_id
FROM fintech.issuers
WHERE country_code = (SELECT country_code 
       FROM fintech.countries 
       WHERE name = 'Colombia'
       LIMIT 1)
       AND name LIKE '%SamsonCorp%'
LIMIT 1;
-- UPDATE
UPDATE fintech.issuers
SET name = 'Banco de Occidente S.A.S'
WHERE issuer_id = 'ISU-5621631365820580507321210';

-- CHECK
SELECT *
FROM fintech.issuers
WHERE issuer_id = 'ISU-5621631365820580507321210';

-- UPDATE FIELDS contact_phone, international set false;



