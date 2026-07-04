-- ============================================================
-- QUESTION 8: Point-in-Time SCD2 JOIN (Slowly Changing Dimension)
-- Difficulty: Super Advanced | Google / MS DE Level
-- ============================================================
--
-- PROBLEM:
-- Your data warehouse stores the products table as SCD Type 2:
-- every time a product's price or category changes, a new row is inserted
-- with updated valid_from and valid_to timestamps.
-- valid_to = NULL means it's the currently active record.
--
-- You have an orders fact table recording all purchases by timestamp.
--
-- Write a query that returns each order with the product's price and category
-- AS IT WAS AT THE TIME THE ORDER WAS PLACED (not the current price).
--
-- Additionally:
--   - Calculate the revenue_at_order_time (quantity * price_at_time_of_order).
--   - Calculate revenue_at_current_price (quantity * current_price).
--   - Show price_drift = revenue_at_current_price - revenue_at_order_time.
--     (Positive drift = product got more expensive. Negative = got cheaper.)
--
-- TRAP 1: Some orders may have been placed BEFORE a product existed in the SCD2 table
--         (data quality issue). These should appear with NULL historical_price and a
--         flag: data_quality_issue = TRUE.
--
-- TRAP 2: Joining on a time range is expensive. Your query must use a
--         non-equi JOIN on: order_time >= valid_from AND (order_time < valid_to OR valid_to IS NULL).
--         Consider how to also get the "current" price in the same query without a second scan.
--
-- This tests: non-equi JOIN on valid time ranges, NULL handling in join conditions,
--             joining to two different versions of the same table (historical + current).
-- ============================================================

CREATE TABLE products_scd2 (
    scd_id INT PRIMARY KEY,
    product_id INT,
    product_name VARCHAR(50),
    category VARCHAR(30),
    unit_price DECIMAL(10, 2),
    valid_from TIMESTAMP,
    valid_to TIMESTAMP -- NULL = currently active
);

INSERT INTO
    products_scd2
VALUES (
        1,
        101,
        'Laptop Pro',
        'Electronics',
        999.00,
        '2023-01-01',
        '2023-06-01'
    ),
    (
        2,
        101,
        'Laptop Pro',
        'Electronics',
        1099.00,
        '2023-06-01',
        '2024-01-01'
    ),
    (
        3,
        101,
        'Laptop Pro',
        'Electronics',
        1199.00,
        '2024-01-01',
        NULL
    ),
    (
        4,
        102,
        'Wireless Mouse',
        'Accessories',
        29.99,
        '2023-01-01',
        '2023-09-01'
    ),
    (
        5,
        102,
        'Wireless Mouse',
        'Accessories',
        24.99,
        '2023-09-01',
        NULL
    ), -- price dropped
    (
        6,
        103,
        'USB-C Hub',
        'Accessories',
        49.99,
        '2023-03-01',
        '2023-12-01'
    ),
    (
        7,
        103,
        'USB-C Hub',
        'Electronics',
        59.99,
        '2023-12-01',
        NULL
    ), -- category changed!
    (
        8,
        104,
        'Desk Chair',
        'Furniture',
        299.00,
        '2023-01-01',
        '2024-02-01'
    ),
    (
        9,
        104,
        'Desk Chair',
        'Furniture',
        349.00,
        '2024-02-01',
        NULL
    ),
    (
        10,
        105,
        'Monitor 27"',
        'Electronics',
        399.00,
        '2023-06-01',
        '2024-03-01'
    ),
    (
        11,
        105,
        'Monitor 27"',
        'Electronics',
        449.00,
        '2024-03-01',
        NULL
    );

CREATE TABLE orders_fact (
    order_id INT PRIMARY KEY,
    customer VARCHAR(50),
    product_id INT,
    quantity INT,
    order_time TIMESTAMP
);

INSERT INTO
    orders_fact
VALUES (
        1,
        'Alice',
        101,
        1,
        '2023-03-15 10:00'
    ), -- Laptop at 999
    (
        2,
        'Bob',
        101,
        2,
        '2023-07-20 14:00'
    ), -- Laptop at 1099
    (
        3,
        'Carol',
        101,
        1,
        '2024-02-01 09:00'
    ), -- Laptop at 1199
    (
        4,
        'Dave',
        102,
        3,
        '2023-05-10 11:00'
    ), -- Mouse at 29.99
    (
        5,
        'Eve',
        102,
        5,
        '2023-10-01 16:00'
    ), -- Mouse at 24.99 (after price drop)
    (
        6,
        'Frank',
        103,
        2,
        '2023-04-20 13:00'
    ), -- USB-C Hub at 49.99, category Accessories
    (
        7,
        'Grace',
        103,
        1,
        '2024-01-15 10:00'
    ), -- USB-C Hub at 59.99, category Electronics
    (
        8,
        'Heidi',
        104,
        1,
        '2023-11-05 09:00'
    ), -- Desk Chair at 299
    (
        9,
        'Ivan',
        104,
        2,
        '2024-03-01 15:00'
    ), -- Desk Chair at 349
    (
        10,
        'Judy',
        105,
        1,
        '2023-08-20 12:00'
    ), -- Monitor at 399
    (
        11,
        'Karl',
        105,
        2,
        '2024-04-10 11:00'
    ), -- Monitor at 449
    (
        12,
        'Laura',
        101,
        1,
        '2022-12-01 10:00'
    ), -- TRAP: Order BEFORE product existed → data_quality_issue
    (
        13,
        'Mallory',
        106,
        1,
        '2024-01-10 10:00'
    ), -- TRAP: product_id 106 doesn't exist → data_quality_issue
    (
        14,
        'Niaj',
        102,
        2,
        '2023-08-31 23:59'
    ), -- Edge case: exactly at boundary of valid_from
    (
        15,
        'Oscar',
        103,
        3,
        '2023-12-01 00:00'
    );
-- Edge case: exactly at SCD2 changeover moment

-- YOUR QUERY HERE: