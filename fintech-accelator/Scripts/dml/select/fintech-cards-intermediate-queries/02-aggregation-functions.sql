-- JOINS APPLICATION
-- DATABASE: FINTECH_CARDS
-- LAST_UPDATED: 10/05/2025


/**
SUM: Calcular el monto total de transacciones realizadas por cada cliente 
en los últimos 3 meses, mostrando el nombre del cliente y el total gastado.
**/
-- FK: (transactions -> credit_cards -> clients)
SELECT
	cl.client_id,
    (cl.first_name ||' '||cl.last_name) AS client,
    COUNT(*) AS total_transactions_done,
    SUM(tr.amount) AS total_amount_spent
FROM 
    fintech.transactions AS tr
INNER JOIN fintech.credit_cards AS cc
    ON tr.card_id = cc.card_id
INNER JOIN fintech.clients AS cl
    ON cc.client_id = cl.client_id
WHERE 
    tr.transaction_date >= (CURRENT_DATE - INTERVAL '3 months')
GROUP BY cl.client_id, cl.first_name, cl.last_name
ORDER BY cl.client_id DESC
LIMIT 5;

-- check specific transactions
SELECT tr.amount, tr.transaction_date, cc.card_id, cc.client_id
FROM fintech.TRANSACTIONS as tr
INNER JOIN fintech.credit_cards AS cc
ON tr.card_id = cc.card_id
WHERE cc.client_id = '  INS-AUTO17924456385';



/**
AVG: Obtener el valor promedio de las transacciones agrupadas por categoría
de comercio y método de pago, para identificar los patrones de gasto según 
el tipo de establecimiento.
**/

/**
COUNT: Contar el número de tarjetas de crédito emitidas por cada entidad 
bancaria (issuer), agrupadas por franquicia, mostrando qué bancos 
tienen mayor presencia por tipo de tarjeta.
**/

/**
MIN y MAX: Mostrar el monto de transacción más bajo y más alto para cada 
cliente, junto con la fecha en que ocurrieron, para identificar patrones 
de gasto extremos.
**/