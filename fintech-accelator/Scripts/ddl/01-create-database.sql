-- 01. Create user
CREATE USER fc_admin WITH PASSWORD '*****';
-- 02. Create database (with ENCODING= 'UTF8', TEMPLATE=Template 0, OWNER: fc_admin)
CREATE DATABASE fintech_cards WITH ENCODING='UTF8' LC_COLLATE='es_CO.UTF-8' LC_CTYPE='es_CO.UTF-8' TEMPLATE=template0 OWNER = fc_admin;
-- 03. Grant privileges
GRANT ALL PRIVILEGES ON DATABASE fintech_cards TO fc_admin;
-- 04. Create Schema
CREATE SCHEMA IF NOT EXISTS fintech AUTHORIZATION fc_admin;
-- 05. Comment on database
COMMENT ON DATABASE fintech_cards IS 'Base de datos para el sistema de transacciones de tarjetas de crédito';
-- 06. Comment of schema
COMMENT ON SCHEMA fintech IS 'Esquema principal para el sistema de transacciones financieras';