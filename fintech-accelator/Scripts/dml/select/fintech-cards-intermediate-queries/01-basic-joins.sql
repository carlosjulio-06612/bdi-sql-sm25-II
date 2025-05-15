-- JOINS APPLICATION
-- DATABASE: FINTECH_CARDS
-- LAST_UPDATED: 10/05/2025

/**
INNER JOIN: Listar todas las transacciones con detalles del cliente, 
incluyendo nombre del cliente, monto de la transacción, 
nombre del comercio y método de pago utilizado.
**/

-- JOIN (transactions -> merchant_locations -> credit_cards -> clients ->payment_methods)
SELECT 
    (cl.first_name ||' '||COALESCE(cl.middle_name, '')||' '||cl.last_name) AS client,
    tr.amount AS transaction_amount,
    ml.store_name AS purchased_store,
    pm.name AS payment_method

FROM fintech.transactions AS tr
    INNER JOIN fintech.merchant_locations AS ml
    ON tr.location_id = ml.location_id
    INNER JOIN fintech.credit_cards AS cc
    ON tr.card_id = cc.card_id
    INNER JOIN fintech.clients AS cl
    ON cl.client_id = cc.client_id
    INNER JOIN fintech.payment_methods AS pm
    ON tr.method_id = pm.method_id

LIMIT 10;

/**
LEFT JOIN: Listar todos los clientes y sus tarjetas de crédito, 
incluyendo aquellos clientes que no tienen ninguna 
tarjeta registrada en el sistema.
**/

/**
RIGHT JOIN: Listar todas las ubicaciones comerciales y las transacciones 
realizadas en ellas, incluyendo aquellas ubicaciones donde 
aún no se han registrado transacciones.
**/

/**
FULL JOIN: Listar todas las franquicias y los países donde operan, 
incluyendo franquicias que no están asociadas a ningún país 
específico y países que no tienen franquicias operando en ellos.
**/

/**
SELF JOIN: Encontrar pares de transacciones realizadas por el mismo 
cliente en la misma ubicación comercial en diferentes
**/

