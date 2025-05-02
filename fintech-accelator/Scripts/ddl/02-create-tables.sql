-- ##################################################
-- #            DDL SCRIPT DOCUMENTATION            #
-- ##################################################
-- This script defines the database structure for a fintech credit card transaction system
-- Includes tables for CLIENTS, CREDIT_CARDS, FRANCHISES, ISSUERS, COUNTRIES, REGIONS, 
-- TRANSACTIONS, MERCHANT_LOCATIONS, and PAYMENT_METHODS, ensuring data integrity,
-- normalization, and performance.
-- The system is designed to track credit card transactions between merchants and customers,
-- with comprehensive reference data for financial institutions, geographical locations,
-- and payment processing details. The structure supports transaction monitoring, fraud detection,
-- and financial analytics with proper relationship constraints.

-- ##################################################
-- #              TABLE DEFINITIONS                 #
-- ##################################################

-- Independent tables first
-- Table: fintech.REGIONS
-- Brief: Stores geographical regions for organizing countries
CREATE TABLE IF NOT EXISTS fintech.REGIONS (
    region_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Table: fintech.COUNTRIES
-- Brief: Stores country information with currency and region association
CREATE TABLE IF NOT EXISTS fintech.COUNTRIES (
    country_code VARCHAR(3) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    region_id INT NULL
);


-- Table: fintech.PAYMENT_METHODS
-- Brief: Reference table for payment method types (e.g., chip, contactless, swipe)
CREATE TABLE IF NOT EXISTS fintech.PAYMENT_METHODS (
    method_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Table: fintech.CLIENTS
-- Brief: Stores customer information who own credit cards
CREATE TABLE IF NOT EXISTS fintech.CLIENTS (
    client_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    birth_date DATE,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    address VARCHAR(255)
);

-- Table: fintech.ISSUERS
-- Brief: Financial institutions that issue credit cards
CREATE TABLE IF NOT EXISTS fintech.ISSUERS (
    issuer_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    bank_code VARCHAR(50) NOT NULL,
    contact_phone VARCHAR(50),
    international BOOLEAN DEFAULT FALSE,
    country_code VARCHAR(3) NOT NULL
);

-- Dependent tables
-- Table: fintech.FRANCHISES
-- Brief: Credit card brands/networks (e.g., Visa, Mastercard)
CREATE TABLE IF NOT EXISTS fintech.FRANCHISES (
    franchise_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    issuer_id VARCHAR(50) NOT NULL,
    country_code VARCHAR(3) NOT NULL
);

-- Table: fintech.MERCHANT_LOCATIONS
-- Brief: Physical or virtual locations where transactions occur
CREATE TABLE IF NOT EXISTS fintech.MERCHANT_LOCATIONS (
    location_id SERIAL PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country_code VARCHAR(3) NOT NULL,
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6)
);

-- Table: fintech.CREDIT_CARDS
-- Brief: Individual credit cards issued to clients
CREATE TABLE IF NOT EXISTS fintech.CREDIT_CARDS (
    card_id VARCHAR(50) PRIMARY KEY,
    client_id VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    expiration_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    franchise_id INT NOT NULL
);

-- Transactional tables
-- Table: fintech.TRANSACTIONS
-- Brief: Records of financial transactions made with credit cards
CREATE TABLE IF NOT EXISTS fintech.TRANSACTIONS (
    transaction_id VARCHAR(50) PRIMARY KEY,
    card_id VARCHAR(50) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    channel VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    device_type VARCHAR(50),
    location_id INT NOT NULL,
    method_id INT NOT NULL
);

-- ##################################################
-- #            RELATIONSHIP DEFINITIONS            #
-- ##################################################

-- Relationships for COUNTRIES
ALTER TABLE fintech.COUNTRIES ADD CONSTRAINT fk_countries_regions 
    FOREIGN KEY (region_id) REFERENCES fintech.REGIONS (region_id);

-- Relationships for ISSUERS
ALTER TABLE fintech.ISSUERS ADD CONSTRAINT fk_issuers_countries 
    FOREIGN KEY (country_code) REFERENCES fintech.COUNTRIES (country_code);

-- Relationships for FRANCHISES
ALTER TABLE fintech.FRANCHISES ADD CONSTRAINT fk_franchises_issuers 
    FOREIGN KEY (issuer_id) REFERENCES fintech.ISSUERS (issuer_id);
ALTER TABLE fintech.FRANCHISES ADD CONSTRAINT fk_franchises_countries 
    FOREIGN KEY (country_code) REFERENCES fintech.COUNTRIES (country_code);

-- Relationships for MERCHANT_LOCATIONS
ALTER TABLE fintech.MERCHANT_LOCATIONS ADD CONSTRAINT fk_locations_countries 
    FOREIGN KEY (country_code) REFERENCES fintech.COUNTRIES (country_code);

-- Relationships for CREDIT_CARDS
ALTER TABLE fintech.CREDIT_CARDS ADD CONSTRAINT fk_cards_clients 
    FOREIGN KEY (client_id) REFERENCES fintech.CLIENTS (client_id);
ALTER TABLE fintech.CREDIT_CARDS ADD CONSTRAINT fk_cards_franchises 
    FOREIGN KEY (franchise_id) REFERENCES fintech.FRANCHISES (franchise_id);

-- Relationships for TRANSACTIONS
ALTER TABLE fintech.TRANSACTIONS ADD CONSTRAINT fk_transactions_cards 
    FOREIGN KEY (card_id) REFERENCES fintech.CREDIT_CARDS (card_id);
ALTER TABLE fintech.TRANSACTIONS ADD CONSTRAINT fk_transactions_locations 
    FOREIGN KEY (location_id) REFERENCES fintech.MERCHANT_LOCATIONS (location_id);
ALTER TABLE fintech.TRANSACTIONS ADD CONSTRAINT fk_transactions_methods 
    FOREIGN KEY (method_id) REFERENCES fintech.PAYMENT_METHODS (method_id);

-- ##################################################
-- #               END DOCUMENTATION                #
-- ##################################################