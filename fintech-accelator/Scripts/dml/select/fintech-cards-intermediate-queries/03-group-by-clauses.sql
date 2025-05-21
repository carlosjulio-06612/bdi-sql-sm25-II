-- JOINS APPLICATION
-- DATABASE: FINTECH_CARDS
-- LAST_UPDATED: 10/05/202

/**
1. Obtener el total de gastos por cliente en los últimos 6 meses, 
mostrando solo aquellos que han gastado más de $5,000, 
incluyendo su nombre completo y cantidad de transacciones realizadas.
*/
SELECT 
    cl.client_id,
    (cl.first_name || ' ' || COALESCE(cl.middle_name, '') || ' ' || cl.last_name) AS full_name,
    COUNT(tr.transaction_id) AS transaction_count,
    SUM(tr.amount) AS total_spent

FROM fintech.transactions AS tr
INNER JOIN fintech.credit_cards AS cc
    ON tr.card_id = cc.card_id
INNER JOIN fintech.clients AS cl
    ON cc.client_id = cl.client_id
WHERE tr.transaction_date >= (CURRENT_DATE - INTERVAL '6 months')
GROUP BY cl.client_id, cl.first_name, cl.middle_name, cl.last_name
HAVING SUM(tr.amount) > 5000
ORDER BY total_spent DESC
LIMIT 20;


/**
2. Listar las categorías de comercios con el promedio de transacciones
por país, mostrando solo aquellas categorías donde el 
promedio de transacción supere los $100 y se hayan 
realizado al menos 50 operaciones.
**/

SELECT
	ml.category,
  AVG(tr.amount) AS avg_transactions,
  COUNT(tr.transaction_id) AS total_operations_made,
  co.name AS country
FROM 
	fintech.merchant_locations AS ml
INNER JOIN fintech.transactions AS tr
	ON ml.location_id = tr.location_id
INNER JOIN fintech.countries AS co
	ON ml.country_code = co.country_code
--WHERE ml.country_code = 'CO' optional filter by colombia
GROUP BY ml.category, co.name
HAVING AVG(tr.amount) > 100
	AND COUNT(tr.transaction_id) >= 50
ORDER BY total_operations_made DESC;


/**
3. Identificar las franquicias de tarjetas con mayor tasa de rechazo 
de transacciones por país, mostrando el nombre de la franquicia, 
país y porcentaje de rechazos, limitando a aquellas 
con más de 5% de rechazos y al menos 100 intentos de transacción.
**/

SELECT 
    total.franchise,
    total.country,
    rejected.rejected_count * 100.0 / total.total_count AS rejection_rate,
    total.total_count AS total_attempts
FROM (
    SELECT 
        fr.name AS franchise,
        co.name AS country,
        COUNT(*) AS total_count
    FROM fintech.transactions tr
    INNER JOIN fintech.credit_cards cc ON tr.card_id = cc.card_id
    INNER JOIN fintech.franchises fr ON cc.franchise_id = fr.franchise_id
    INNER JOIN fintech.merchant_locations ml ON tr.location_id = ml.location_id
    INNER JOIN fintech.countries co ON ml.country_code = co.country_code
    GROUP BY fr.name, co.name
) AS total
INNER JOIN (
    SELECT 
        fr.name AS franchise,
        co.name AS country,
        COUNT(*) AS rejected_count
    FROM fintech.transactions tr
    INNER JOIN fintech.credit_cards cc ON tr.card_id = cc.card_id
    INNER JOIN fintech.franchises fr ON cc.franchise_id = fr.franchise_id
    INNER JOIN fintech.merchant_locations ml ON tr.location_id = ml.location_id
    INNER JOIN fintech.countries co ON ml.country_code = co.country_code
    WHERE tr.status = 'Rejected'
    GROUP BY fr.name, co.name
) AS rejected
ON total.franchise = rejected.franchise AND total.country = rejected.country
WHERE total.total_count >= 100
  AND rejected.rejected_count * 100.0 / total.total_count > 5
ORDER BY rejection_rate DESC


/**
4. Mostrar los métodos de pago más utilizados por cada ciudad, 
incluyendo el nombre del método, ciudad, país y cantidad de 
transacciones, filtrando solo aquellas
combinaciones que representen más del 20% .
del total de transacciones de esa ciudad.
**/
SELECT 
    pm.name AS payment_method,
    ml.city,
    co.name AS country,
    COUNT(*) AS method_count,
    ROUND(COUNT(*) * 100.0 / city_total.total_count, 2) AS method_percentage
FROM fintech.transactions tr
INNER JOIN fintech.payment_methods pm ON tr.method_id = pm.method_id
INNER JOIN fintech.merchant_locations ml ON tr.location_id = ml.location_id
INNER JOIN fintech.countries co ON ml.country_code = co.country_code
INNER JOIN (
    SELECT 
        ml.city,
        COUNT(*) AS total_count
    FROM fintech.transactions tr2
    INNER JOIN fintech.merchant_locations ml ON tr2.location_id = ml.location_id
    GROUP BY ml.city
) AS city_total ON ml.city = city_total.city
GROUP BY pm.name, ml.city, co.name, city_total.total_count
HAVING COUNT(*) * 1.0 / city_total.total_count > 0.20
ORDER BY ml.city, method_percentage DESC
LIMIT 5;
/**
5. Analizar el comportamiento de compra por género y rango de edad, 
mostrando el total gastado, promedio por transacción y número de operaciones 
completadas, incluyendo solo los grupos demográficos 
que tengan al menos 30 clientes activos.
**/
-- Grupo 18-25
SELECT 
    cl.gender,
    '18-25' AS age_group,
    COUNT(DISTINCT cl.client_id) AS clients_in_group,
    COUNT(tr.transaction_id) AS total_transactions,
    SUM(tr.amount) AS total_spent,
    AVG(tr.amount) AS avg_per_transaction
FROM fintech.clients cl
INNER JOIN fintech.credit_cards cc ON cl.client_id = cc.client_id
INNER JOIN fintech.transactions tr ON cc.card_id = tr.card_id
WHERE DATE_PART('year', AGE(CURRENT_DATE, cl.birth_date)) >= 18
  AND DATE_PART('year', AGE(CURRENT_DATE, cl.birth_date)) <= 25
GROUP BY cl.gender
HAVING COUNT(DISTINCT cl.client_id) >= 30

UNION ALL

-- Grupo 26-35
SELECT 
    cl.gender,
    '26-35' AS age_group,
    COUNT(DISTINCT cl.client_id),
    COUNT(tr.transaction_id),
    SUM(tr.amount),
    AVG(tr.amount)
FROM fintech.clients cl
INNER JOIN fintech.credit_cards cc ON cl.client_id = cc.client_id
INNER JOIN fintech.transactions tr ON cc.card_id = tr.card_id
WHERE DATE_PART('year', AGE(CURRENT_DATE, cl.birth_date)) >= 26
  AND DATE_PART('year', AGE(CURRENT_DATE, cl.birth_date)) <= 35
GROUP BY cl.gender
HAVING COUNT(DISTINCT cl.client_id) >= 30

UNION ALL

-- Grupo 36-50
SELECT 
    cl.gender,
    '36-50' AS age_group,
    COUNT(DISTINCT cl.client_id),
    COUNT(tr.transaction_id),
    SUM(tr.amount),
    AVG(tr.amount)
FROM fintech.clients cl
INNER JOIN fintech.credit_cards cc ON cl.client_id = cc.client_id
INNER JOIN fintech.transactions tr ON cc.card_id = tr.card_id
WHERE DATE_PART('year', AGE(CURRENT_DATE, cl.birth_date)) >= 36
  AND DATE_PART('year', AGE(CURRENT_DATE, cl.birth_date)) <= 50
GROUP BY cl.gender
HAVING COUNT(DISTINCT cl.client_id) >= 30

UNION ALL

-- Grupo 50+
SELECT 
    cl.gender,
    '50+' AS age_group,
    COUNT(DISTINCT cl.client_id),
    COUNT(tr.transaction_id),
    SUM(tr.amount),
    AVG(tr.amount)
FROM fintech.clients cl
INNER JOIN fintech.credit_cards cc ON cl.client_id = cc.client_id
INNER JOIN fintech.transactions tr ON cc.card_id = tr.card_id
WHERE DATE_PART('year', AGE(CURRENT_DATE, cl.birth_date)) > 50
GROUP BY cl.gender
HAVING COUNT(DISTINCT cl.client_id) >= 30;
