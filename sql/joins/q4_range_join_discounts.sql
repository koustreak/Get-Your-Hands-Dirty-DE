-- ============================================================
-- QUESTION 4: Assign Price Brackets via Range JOIN (Non-Equi JOIN)
-- Difficulty: Advanced | Google / MS DE Level
-- ============================================================
--
-- PROBLEM:
-- You have a products table and a discount_rules table.
-- Each discount rule applies to orders where the total_amount falls
-- within a price bracket (min_amount <= total < max_amount).
-- Additionally, the discount rule has a category_match — if category_match
-- is NULL, it applies to ALL categories. If set, it applies only to that category.
--
-- For each order, find the BEST applicable discount rule:
--   - A category-specific rule always beats a category-agnostic (NULL) rule.
--   - Among rules of the same specificity, pick the one with the highest discount_pct.
--
-- Return: order_id, customer_name, total_amount, category,
--         applied_rule_id, discount_pct, final_amount_after_discount.
--
-- Orders with NO applicable discount rule should still appear with NULL discount info.
--
-- This tests: non-equi JOIN on ranges, multi-condition join, priority/ranking over join results.
-- ============================================================

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(50),
    category VARCHAR(30),
    total_amount DECIMAL(10, 2)
);

INSERT INTO
    orders
VALUES (
        1,
        'Alice',
        'Electronics',
        85.00
    ),
    (
        2,
        'Bob',
        'Electronics',
        320.00
    ),
    (3, 'Carol', 'Clothing', 45.00),
    (4, 'Dave', 'Clothing', 210.00),
    (5, 'Eve', 'Books', 15.00),
    (6, 'Frank', 'Books', 75.00),
    (
        7,
        'Grace',
        'Electronics',
        520.00
    ),
    (
        8,
        'Heidi',
        'Furniture',
        950.00
    ),
    (
        9,
        'Ivan',
        'Furniture',
        150.00
    ),
    (
        10,
        'Judy',
        'Clothing',
        500.00
    ),
    (
        11,
        'Karl',
        'Electronics',
        1200.00
    ),
    (12, 'Laura', 'Books', 5.00),
    (
        13,
        'Mallory',
        'Furniture',
        2500.00
    ),
    (
        14,
        'Niaj',
        'Electronics',
        99.99
    ),
    (
        15,
        'Oscar',
        'Clothing',
        750.00
    );

CREATE TABLE discount_rules (
    rule_id INT PRIMARY KEY,
    category_match VARCHAR(30), -- NULL = applies to all categories
    min_amount DECIMAL(10, 2),
    max_amount DECIMAL(10, 2),
    discount_pct DECIMAL(5, 2)
);

INSERT INTO
    discount_rules
VALUES (1, NULL, 50.00, 200.00, 5.00), -- Global: 5% for $50-$200
    (2, NULL, 200.00, 500.00, 8.00), -- Global: 8% for $200-$500
    (
        3,
        NULL,
        500.00,
        1000.00,
        12.00
    ), -- Global: 12% for $500-$1000
    (
        4,
        NULL,
        1000.00,
        9999.00,
        15.00
    ), -- Global: 15% for $1000+
    (
        5,
        'Electronics',
        50.00,
        200.00,
        10.00
    ), -- Electronics: 10% for $50-$200 (beats rule 1)
    (
        6,
        'Electronics',
        200.00,
        600.00,
        18.00
    ), -- Electronics: 18% for $200-$600 (beats rule 2)
    (
        7,
        'Electronics',
        600.00,
        9999.00,
        22.00
    ), -- Electronics: 22% for $600+
    (
        8,
        'Clothing',
        100.00,
        400.00,
        7.00
    ), -- Clothing 7% for $100-$400 (beats rule 1 but not rule 2)
    (
        9,
        'Clothing',
        400.00,
        9999.00,
        20.00
    ), -- Clothing 20% for $400+
    (
        10,
        'Books',
        10.00,
        50.00,
        3.00
    ), -- Books: small discount
    (
        11,
        'Furniture',
        500.00,
        1500.00,
        25.00
    ), -- Furniture: 25% for $500-$1500
    (
        12,
        'Furniture',
        1500.00,
        9999.00,
        30.00
    );
-- Furniture: 30% for $1500+

-- YOUR QUERY HERE: