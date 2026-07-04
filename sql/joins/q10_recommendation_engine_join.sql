-- ============================================================
-- QUESTION 10: The N-Way Recommendation Engine (Multi-Table Triangular JOIN)
-- Difficulty: Legendary | Google / MS DE Level
-- ============================================================
--
-- PROBLEM:
-- You are building a product recommendation engine using purchase co-occurrence.
-- "If users who bought product A also frequently bought product B, recommend B to
--  users who bought A but haven't bought B yet."
--
-- Step 1 — Build the co-occurrence matrix:
--   For every ordered pair (product_A, product_B), count how many DISTINCT users
--   bought BOTH products (in any order, in any of their orders).
--   Exclude pairs where product_A = product_B.
--
-- Step 2 — Generate recommendations:
--   For each (user, product_A) where the user HAS bought product_A,
--   recommend the top 3 products by co-occurrence score with product_A,
--   EXCLUDING products the user has already bought.
--
-- Return: user_id, purchased_product, recommended_product, co_occurrence_count, rank
-- Only show rank 1, 2, 3 per (user, purchased_product).
-- Order by user_id, purchased_product, rank.
--
-- This tests: self-join on a purchases table to build co-occurrence,
--             three-way join (user × their products × recommendations),
--             anti-join to exclude already-owned products,
--             and windowed ranking over join results.
-- ============================================================

CREATE TABLE user_purchases (
    purchase_id INT PRIMARY KEY,
    user_id INT,
    product_id INT,
    product_name VARCHAR(50),
    purchase_date DATE
);

INSERT INTO
    user_purchases
VALUES (
        1,
        201,
        1,
        'Laptop',
        '2024-01-05'
    ),
    (
        2,
        201,
        2,
        'Mouse',
        '2024-01-05'
    ),
    (
        3,
        201,
        3,
        'Keyboard',
        '2024-01-10'
    ),
    (
        4,
        202,
        1,
        'Laptop',
        '2024-01-08'
    ),
    (
        5,
        202,
        4,
        'Monitor',
        '2024-01-08'
    ),
    (
        6,
        202,
        2,
        'Mouse',
        '2024-01-15'
    ),
    (
        7,
        203,
        2,
        'Mouse',
        '2024-01-06'
    ),
    (
        8,
        203,
        3,
        'Keyboard',
        '2024-01-06'
    ),
    (
        9,
        203,
        5,
        'Webcam',
        '2024-01-20'
    ),
    (
        10,
        204,
        1,
        'Laptop',
        '2024-01-09'
    ),
    (
        11,
        204,
        3,
        'Keyboard',
        '2024-01-09'
    ),
    (
        12,
        204,
        4,
        'Monitor',
        '2024-01-09'
    ),
    (
        13,
        204,
        5,
        'Webcam',
        '2024-01-25'
    ),
    (
        14,
        205,
        4,
        'Monitor',
        '2024-01-10'
    ),
    (
        15,
        205,
        5,
        'Webcam',
        '2024-01-10'
    ),
    (
        16,
        205,
        6,
        'Speakers',
        '2024-01-10'
    ),
    (
        17,
        206,
        1,
        'Laptop',
        '2024-01-12'
    ),
    (
        18,
        206,
        5,
        'Webcam',
        '2024-01-12'
    ),
    (
        19,
        206,
        6,
        'Speakers',
        '2024-01-20'
    ),
    (
        20,
        207,
        2,
        'Mouse',
        '2024-01-14'
    ),
    (
        21,
        207,
        4,
        'Monitor',
        '2024-01-14'
    ),
    (
        22,
        207,
        6,
        'Speakers',
        '2024-01-22'
    ),
    (
        23,
        208,
        3,
        'Keyboard',
        '2024-01-07'
    ),
    (
        24,
        208,
        5,
        'Webcam',
        '2024-01-07'
    ),
    (
        25,
        208,
        6,
        'Speakers',
        '2024-01-07'
    ),
    (
        26,
        209,
        1,
        'Laptop',
        '2024-01-11'
    ),
    (
        27,
        209,
        2,
        'Mouse',
        '2024-01-11'
    ),
    (
        28,
        210,
        3,
        'Keyboard',
        '2024-01-13'
    ),
    (
        29,
        210,
        4,
        'Monitor',
        '2024-01-13'
    );
-- NOTE: User 209 has only Laptop + Mouse.
--       User 210 has only Keyboard + Monitor.
--       These users should get recommendations from the co-occurrence matrix.

-- YOUR QUERY HERE: