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
    fr.name AS franchise,
    co.name AS country,
    COUNT(*) FILTER (WHERE tr.status = 'Rejected') * 100.0 / COUNT(*) AS rejection_rate,
    COUNT(*) AS total_attempts

FROM fintech.transactions AS tr
INNER JOIN fintech.credit_cards AS cc
    ON tr.card_id = cc.card_id
INNER JOIN fintech.franchises AS fr
    ON cc.franchise_id = fr.franchise_id
INNER JOIN fintech.merchant_locations AS ml
    ON tr.location_id = ml.location_id
INNER JOIN fintech.countries AS co
    ON ml.country_code = co.country_code
GROUP BY fr.name, co.name
HAVING COUNT(*) >= 100 AND 
       COUNT(*) FILTER (WHERE tr.status = 'Rejected') * 100.0 / COUNT(*) > 5
ORDER BY rejection_rate DESC
LIMIT 20;


/**
4. Mostrar los métodos de pago más utilizados por cada ciudad, 
incluyendo el nombre del método, ciudad, país y cantidad de 
transacciones, filtrando solo aquellas
combinaciones que representen más del 20% .
del total de transacciones de esa ciudad.
**/
WITH city_totals AS (
    SELECT 
        city,
        COUNT(*) AS total_transactions
    FROM fintech.transactions tr
    INNER JOIN fintech.merchant_locations ml ON tr.location_id = ml.location_id
    GROUP BY city
)
SELECT 
    pm.name AS payment_method,
    ml.city,
    co.name AS country,
    COUNT(*) AS method_count,
    ROUND(COUNT(*) * 100.0 / ct.total_transactions, 2) AS method_percentage
FROM fintech.transactions tr
INNER JOIN fintech.payment_methods pm ON tr.method_id = pm.method_id
INNER JOIN fintech.merchant_locations ml ON tr.location_id = ml.location_id
INNER JOIN fintech.countries co ON ml.country_code = co.country_code
INNER JOIN city_totals ct ON ml.city = ct.city
GROUP BY pm.name, ml.city, co.name, ct.total_transactions
HAVING COUNT(*) * 1.0 / ct.total_transactions > 0.20
ORDER BY ml.city, method_percentage DESC
LIMIT 20;

/**
5. Analizar el comportamiento de compra por género y rango de edad, 
mostrando el total gastado, promedio por transacción y número de operaciones 
completadas, incluyendo solo los grupos demográficos 
que tengan al menos 30 clientes activos.
**/

SELECT 
    cl.gender,
    CASE
        WHEN DATE_PART('year', AGE(CURRENT_DATE, cl.birth_date)) BETWEEN 18 AND 25 THEN '18-25'
        WHEN DATE_PART('year', AGE(CURRENT_DATE, cl.birth_date)) BETWEEN 26 AND 35 THEN '26-35'
        WHEN DATE_PART('year', AGE(CURRENT_DATE, cl.birth_date)) BETWEEN 36 AND 50 THEN '36-50'
        WHEN DATE_PART('year', AGE(CURRENT_DATE, cl.birth_date)) > 50 THEN '50+'
        ELSE 'Unknown'
    END AS age_group,

    COUNT(DISTINCT cl.client_id) AS clients_in_group,
    COUNT(tr.transaction_id) AS total_transactions,
    SUM(tr.amount) AS total_spent,
    AVG(tr.amount) AS avg_per_transaction

FROM fintech.clients AS cl
INNER JOIN fintech.credit_cards AS cc 
    ON cl.client_id = cc.client_id
INNER JOIN fintech.transactions AS tr 
    ON cc.card_id = tr.card_id
GROUP BY cl.gender, age_group
ORDER BY clients_in_group DESC;
