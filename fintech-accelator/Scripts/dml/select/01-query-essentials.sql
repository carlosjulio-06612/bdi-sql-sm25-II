-- 1. Check total countries

SELECT COUNT(*) AS total_countries
FROM fintech.countries;

-- 2. Count of all issuers that operates in New Zeland and USA
-- COUNTRY_CODES = NZ,US

SELECT country_code AS country_operates,
			 COUNT(*) AS total_issuers_operates
FROM fintech.issuers
WHERE country_code IN ('NZ','US')
GROUP BY country_code;

-- 3. Get the clients that first_name starts with A and end in o
-- only the first 5 records;
SELECT *
FROM fintech.clients
WHERE first_name LIKE 'A%_o';

-- 4. List the first 10 merchant_locations that in categories like
-- Corner, Gallery, Warehouse and Market. Also, exclude all countries
-- except Colombia.
SELECT *
FROM fintech.merchant_locations
WHERE category IN ('Corner','Gallery','Warehouse','Market')
AND country_code = 'CO'
ORDER BY location_id
LIMIT 10;

-- 5. Count credit cards issued by this franquise '886287'alfa2024*
SELECT COUNT(*) AS total_issued_credit_cards
FROM fintech.credit_cards
WHERE franchise_id = 886287;