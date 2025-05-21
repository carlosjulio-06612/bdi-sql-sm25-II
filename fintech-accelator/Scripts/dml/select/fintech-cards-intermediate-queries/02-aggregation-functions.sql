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
SELECT 
    AVG(tr.amount) AS average_amount, 
    pm.name AS payment_method, ml.store_name AS commerce_name, 
    ml.category AS merchant_category
    
FROM fintech.transactions tr
    INNER JOIN fintech.merchant_locations ml
    ON tr.location_id = ml.location_id
    INNER JOIN fintech.payment_methods pm
    ON tr.method_id = pm.method_id

GROUP BY payment_method, commerce_name,merchant_category

ORDER BY average_amount DESC


/**
COUNT: Contar el número de tarjetas de crédito emitidas por cada entidad 
bancaria (issuer), agrupadas por franquicia, mostrando qué bancos 
tienen mayor presencia por tipo de tarjeta.
**/
SELECT
    fr.name AS franchise_name,
    isr.name AS issuer_name, COUNT(cc.card_id) AS total_card_issuer

FROM fintech.credit_cards cc
    INNER JOIN fintech.franchises fr ON cc.franchise_id = fr.franchise_id
    INNER JOIN fintech.issuers isr ON fr.issuer_id = isr.issuer_id
GROUP BY fr.name, isr.name
ORDER BY fr.name, total_card_issuer DESC;

/**
MIN y MAX: Mostrar el monto de transacción más bajo y más alto para cada 
cliente, junto con la fecha en que ocurrieron, para identificar patrones 
de gasto extremos.
**/
SELECT
    (cl.first_name || ' ' || cl.last_name) AS client_name,
    MIN(tr.amount) AS overall_minimum_amount,
	(SELECT 
		sub_tr.transaction_date
     FROM fintech.transactions sub_tr
     	INNER JOIN fintech.credit_cards sub_cc 
	 	ON sub_tr.card_id = sub_cc.card_id
     WHERE sub_cc.client_id = cl.client_id
       AND sub_tr.amount = MIN(tr.amount)
     ORDER BY sub_tr.transaction_date ASC
     LIMIT 1
    ) AS min_transaction_date,

    MAX(tr.amount) AS overall_maximum_amount,
    (SELECT 
		sub_tr.transaction_date
     FROM fintech.transactions sub_tr
     	INNER JOIN fintech.credit_cards sub_cc 
		ON sub_tr.card_id = sub_cc.card_id
     WHERE sub_cc.client_id = cl.client_id
       AND sub_tr.amount = MAX(tr.amount) 
     ORDER BY sub_tr.transaction_date DESC 
     LIMIT 1
    ) AS max_transaction_date
FROM fintech.clients cl
	INNER JOIN fintech.credit_cards cc 
	ON cl.client_id = cc.client_id
	INNER JOIN fintech.transactions tr 
	ON cc.card_id = tr.card_id
	GROUP BY cl.client_id, cl.first_name, cl.last_name 
ORDER BY overall_maximum_amount DESC, client_name
