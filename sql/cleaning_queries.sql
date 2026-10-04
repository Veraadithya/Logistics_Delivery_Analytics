USE retail_logistics;

-- ============================================================
-- RETAIL LOGISTICS DATA CLEANING & QUALITY QUERIES
-- ============================================================


-- 1. CHECK TOTAL RECORDS
SELECT
    COUNT(*) AS total_records
FROM logistics_analytics;


-- 2. CHECK DUPLICATE ORDER + PRODUCT RECORDS
SELECT
    order_id,
    product_id,
    COUNT(*) AS duplicate_count
FROM logistics_analytics
GROUP BY order_id, product_id
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;


-- 3. CHECK MISSING ORDER IDs
SELECT
    COUNT(*) AS missing_order_ids
FROM logistics_analytics
WHERE order_id IS NULL
   OR TRIM(order_id) = '';


-- 4. CHECK MISSING CUSTOMER IDs
SELECT
    COUNT(*) AS missing_customer_ids
FROM logistics_analytics
WHERE customer_id IS NULL
   OR TRIM(customer_id) = '';


-- 5. CHECK MISSING SELLER IDs
SELECT
    COUNT(*) AS missing_seller_ids
FROM logistics_analytics
WHERE seller_id IS NULL
   OR TRIM(seller_id) = '';


-- 6. CHECK MISSING PRODUCT IDs
SELECT
    COUNT(*) AS missing_product_ids
FROM logistics_analytics
WHERE product_id IS NULL
   OR TRIM(product_id) = '';


-- 7. CHECK INVALID DELIVERY DAYS
SELECT
    order_id,
    delivery_days
FROM logistics_analytics
WHERE delivery_days < 0
ORDER BY delivery_days;


-- 8. CHECK INVALID DELAY DAYS
SELECT
    order_id,
    delay_days
FROM logistics_analytics
WHERE delay_days < -100
   OR delay_days > 365
ORDER BY delay_days DESC;


-- 9. CHECK DELIVERY DATE BEFORE PURCHASE DATE
SELECT
    order_id,
    order_purchase_timestamp,
    order_delivered_customer_date
FROM logistics_analytics
WHERE order_delivered_customer_date
      < order_purchase_timestamp;


-- 10. CHECK ESTIMATED DELIVERY DATE BEFORE PURCHASE DATE
SELECT
    order_id,
    order_purchase_timestamp,
    order_estimated_delivery_date
FROM logistics_analytics
WHERE order_estimated_delivery_date
      < order_purchase_timestamp;


-- 11. CHECK MISSING DELIVERY STATUS
SELECT
    COUNT(*) AS missing_delivery_status
FROM logistics_analytics
WHERE delivery_status IS NULL
   OR TRIM(delivery_status) = '';


-- 12. CHECK INVALID DELIVERY STATUS VALUES
SELECT DISTINCT
    delivery_status
FROM logistics_analytics
ORDER BY delivery_status;


-- 13. CHECK NEGATIVE PRODUCT PRICES
SELECT
    order_id,
    product_id,
    price
FROM logistics_analytics
WHERE price < 0;


-- 14. CHECK NEGATIVE FREIGHT VALUES
SELECT
    order_id,
    freight_value
FROM logistics_analytics
WHERE freight_value < 0;


-- 15. CHECK INVALID REVIEW SCORES
SELECT
    order_id,
    review_score
FROM logistics_analytics
WHERE review_score IS NOT NULL
  AND (review_score < 1 OR review_score > 5);


-- 16. CHECK MISSING PRODUCT CATEGORIES
SELECT
    COUNT(*) AS missing_product_categories
FROM logistics_analytics
WHERE product_category_name_english IS NULL
   OR TRIM(product_category_name_english) = '';


-- 17. CHECK VERY LONG DELIVERIES
SELECT
    order_id,
    delivery_days
FROM logistics_analytics
WHERE delivery_days > 60
ORDER BY delivery_days DESC;


-- 18. CHECK EXTREME DELIVERY DELAYS
SELECT
    order_id,
    delay_days,
    delivery_status
FROM logistics_analytics
WHERE delay_days > 30
ORDER BY delay_days DESC;


-- 19. CHECK OVERALL DATA QUALITY SUMMARY
SELECT
    COUNT(*) AS total_records,

    SUM(
        CASE
            WHEN order_id IS NULL OR TRIM(order_id) = ''
            THEN 1 ELSE 0
        END
    ) AS missing_order_ids,

    SUM(
        CASE
            WHEN customer_id IS NULL OR TRIM(customer_id) = ''
            THEN 1 ELSE 0
        END
    ) AS missing_customer_ids,

    SUM(
        CASE
            WHEN seller_id IS NULL OR TRIM(seller_id) = ''
            THEN 1 ELSE 0
        END
    ) AS missing_seller_ids,

    SUM(
        CASE
            WHEN delivery_days < 0
            THEN 1 ELSE 0
        END
    ) AS invalid_delivery_days,

    SUM(
        CASE
            WHEN price < 0
            THEN 1 ELSE 0
        END
    ) AS negative_prices,

    SUM(
        CASE
            WHEN freight_value < 0
            THEN 1 ELSE 0
        END
    ) AS negative_freight_values

FROM logistics_analytics;


-- 20. FINAL DATA QUALITY STATUS
SELECT
    CASE
        WHEN
            SUM(
                CASE
                    WHEN order_id IS NULL
                      OR customer_id IS NULL
                      OR seller_id IS NULL
                      OR delivery_days < 0
                      OR price < 0
                      OR freight_value < 0
                    THEN 1 ELSE 0
                END
            ) = 0
        THEN 'PASS'
        ELSE 'CHECK REQUIRED'
    END AS data_quality_status
FROM logistics_analytics;