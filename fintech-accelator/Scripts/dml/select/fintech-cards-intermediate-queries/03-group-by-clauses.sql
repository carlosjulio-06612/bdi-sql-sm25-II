-- JOINS APPLICATION
-- DATABASE: FINTECH_CARDS
-- LAST_UPDATED: 10/05/202

/**
1. Obtener el total de gastos por cliente en los últimos 6 meses, 
mostrando solo aquellos que han gastado más de $5,000, 
incluyendo su nombre completo y cantidad de transacciones realizadas.
*/


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

/**
4. Mostrar los métodos de pago más utilizados por cada ciudad, 
incluyendo el nombre del método, ciudad, país y cantidad de 
transacciones, filtrando solo aquellas
combinaciones que representen más del 20% .
del total de transacciones de esa ciudad.
**/

/**
Analizar el comportamiento de compra por género y rango de edad, 
mostrando el total gastado, promedio por transacción y número de operaciones 
completadas, incluyendo solo los grupos demográficos 
que tengan al menos 30 clientes activos.
**/