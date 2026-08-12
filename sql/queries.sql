-- MLOps - Olist Dataset
-- Basic SQL Queries

-- 1. Preview customer data
SELECT *
FROM customers
LIMIT 5;

-- 2. Count the total number of orders
SELECT COUNT(*)
FROM orders;

-- 3. Join orders with customers
SELECT
    orders.order_id,
    orders.order_status,
    customers.customer_city,
    customers.customer_state
FROM orders
JOIN customers
    ON orders.customer_id = customers.customer_id
LIMIT 5;