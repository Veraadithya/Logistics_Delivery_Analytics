SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(delay_days), 2) AS avg_delay_days,
    SUM(CASE
        WHEN delivery_status = 'Late' THEN 1
        ELSE 0
    END) AS late_orders
FROM logistics_analytics;
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN delivery_status = 'Late' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM logistics_analytics;
SELECT
    seller_id,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(delay_days), 2) AS avg_delay_days,
    SUM(
        CASE
            WHEN delivery_status = 'Late' THEN 1
            ELSE 0
        END
    ) AS late_orders
FROM logistics_analytics
GROUP BY seller_id
ORDER BY late_orders DESC;
SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(delay_days), 2) AS avg_delay_days
FROM logistics_analytics
GROUP BY customer_state
ORDER BY avg_delay_days DESC;
SELECT
    product_category_name_english AS category,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(delay_days), 2) AS avg_delay_days
FROM logistics_analytics
WHERE product_category_name_english IS NOT NULL
GROUP BY product_category_name_english
ORDER BY avg_delay_days DESC;
SELECT
    CASE
        WHEN freight_value < 10 THEN 'Low Freight'
        WHEN freight_value < 30 THEN 'Medium Freight'
        ELSE 'High Freight'
    END AS freight_group,
    COUNT(*) AS orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(delay_days), 2) AS avg_delay_days
FROM logistics_analytics
GROUP BY
    CASE
        WHEN freight_value < 10 THEN 'Low Freight'
        WHEN freight_value < 30 THEN 'Medium Freight'
        ELSE 'High Freight'
    END;
    SELECT
    delivery_status,
    COUNT(*) AS orders,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM logistics_analytics
WHERE review_score IS NOT NULL
GROUP BY delivery_status;