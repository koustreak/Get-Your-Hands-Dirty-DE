-- ============================================================
-- QUESTION 5: The Missing Dimension (CROSS JOIN + Anti-Pattern)
-- Difficulty: Advanced | Google / MS DE Level
-- ============================================================
--
-- PROBLEM:
-- You have a sales table recording (product, region, month, revenue).
-- NOT every product-region combination has a record for every month.
-- Missing combinations mean zero sales that month.
--
-- Write a query that produces a COMPLETE grid:
--   - Every product × every region × every month (Jan to Jun 2024).
--   - Show revenue = 0 for combinations with no recorded sales.
--   - Additionally, for each product-region pair, show:
--       * total_revenue       (sum across all 6 months)
--       * months_with_sales   (count of months with revenue > 0)
--       * best_month          (the month with the highest revenue for that pair)
--       * worst_active_month  (the month with the LOWEST non-zero revenue for that pair)
--
-- TRAP: There are some product-region pairs that have ZERO sales in ALL 6 months.
--       They must still appear in the output (total_revenue=0, months_with_sales=0,
--       best_month=NULL, worst_active_month=NULL).
--
-- This tests: CROSS JOIN to build the complete grid, LEFT JOIN to fill real data,
--             COALESCE for nulls, and conditional aggregation.
-- ============================================================

CREATE TABLE products_dim ( product VARCHAR(30) PRIMARY KEY );

CREATE TABLE regions_dim ( region VARCHAR(30) PRIMARY KEY );

INSERT INTO
    products_dim
VALUES ('Laptop'),
    ('Phone'),
    ('Tablet'),
    ('Monitor'),
    ('Headphones');

INSERT INTO
    regions_dim
VALUES ('North'),
    ('South'),
    ('East'),
    ('West'),
    ('Central');

CREATE TABLE monthly_sales (
    product VARCHAR(30),
    region VARCHAR(30),
    sale_month DATE, -- First day of the month: '2024-01-01'
    revenue DECIMAL(12, 2),
    PRIMARY KEY (product, region, sale_month)
);

INSERT INTO
    monthly_sales
VALUES (
        'Laptop',
        'North',
        '2024-01-01',
        12000
    ),
    (
        'Laptop',
        'North',
        '2024-02-01',
        15000
    ),
    (
        'Laptop',
        'North',
        '2024-03-01',
        9000
    ),
    (
        'Laptop',
        'South',
        '2024-01-01',
        8000
    ),
    (
        'Laptop',
        'South',
        '2024-03-01',
        11000
    ),
    (
        'Laptop',
        'East',
        '2024-02-01',
        7000
    ),
    (
        'Laptop',
        'East',
        '2024-04-01',
        13000
    ),
    (
        'Phone',
        'North',
        '2024-01-01',
        22000
    ),
    (
        'Phone',
        'North',
        '2024-02-01',
        18000
    ),
    (
        'Phone',
        'South',
        '2024-01-01',
        15000
    ),
    (
        'Phone',
        'South',
        '2024-02-01',
        19000
    ),
    (
        'Phone',
        'South',
        '2024-03-01',
        21000
    ),
    (
        'Phone',
        'Central',
        '2024-05-01',
        5000
    ),
    (
        'Tablet',
        'West',
        '2024-01-01',
        4000
    ),
    (
        'Tablet',
        'West',
        '2024-02-01',
        4500
    ),
    (
        'Tablet',
        'West',
        '2024-03-01',
        3800
    ),
    (
        'Tablet',
        'West',
        '2024-04-01',
        5200
    ),
    (
        'Tablet',
        'East',
        '2024-02-01',
        3200
    ),
    (
        'Monitor',
        'North',
        '2024-03-01',
        6500
    ),
    (
        'Monitor',
        'North',
        '2024-06-01',
        7100
    ),
    (
        'Monitor',
        'South',
        '2024-04-01',
        5800
    ),
    (
        'Headphones',
        'Central',
        '2024-01-01',
        3100
    ),
    (
        'Headphones',
        'Central',
        '2024-04-01',
        2900
    ),
    (
        'Headphones',
        'North',
        '2024-06-01',
        1800
    );
-- NOTE: 'Monitor' has ZERO sales in West/East/Central. 'Tablet' has ZERO in North/South/Central.
-- 'Headphones' has zero in South/East/West.

-- YOUR QUERY HERE: