-- ============================================================
-- RETAIL LOGISTICS DELIVERY ANALYTICS
-- DATABASE SCHEMA
-- ============================================================

-- Create database
CREATE DATABASE IF NOT EXISTS retail_logistics;

-- Select database
USE retail_logistics;


-- ============================================================
-- MAIN ANALYTICS TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS logistics_analytics (

    order_id VARCHAR(50),
    customer_id VARCHAR(50),
    seller_id VARCHAR(50),
    product_id VARCHAR(50),

    order_status VARCHAR(30),

    order_purchase_timestamp DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME,

    delivery_days DECIMAL(10,2),
    delay_days DECIMAL(10,2),

    delivery_status VARCHAR(20),

    product_category_name_english VARCHAR(150),

    price DECIMAL(10,2),
    freight_value DECIMAL(10,2),

    customer_city VARCHAR(100),
    customer_state VARCHAR(10),

    seller_city VARCHAR(100),
    seller_state VARCHAR(10),

    review_score INT
);


-- ============================================================
-- VERIFY DATABASE
-- ============================================================

SELECT DATABASE();


-- ============================================================
-- VERIFY TABLE
-- ============================================================

SHOW TABLES;


-- ============================================================
-- CHECK TABLE STRUCTURE
-- ============================================================

DESCRIBE logistics_analytics;


-- ============================================================
-- CHECK NUMBER OF RECORDS
-- ============================================================

SELECT
    COUNT(*) AS total_records
FROM logistics_analytics;