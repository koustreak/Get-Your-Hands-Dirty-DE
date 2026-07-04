-- ============================================================
-- QUESTION 9: FULL OUTER JOIN Reconciliation (Data Pipeline Audit)
-- Difficulty: Legendary | Google / MS DE Level
-- ============================================================
--
-- PROBLEM:
-- You run a daily ETL pipeline that syncs data from a source system to a warehouse.
-- After a pipeline run, you need to RECONCILE the source table vs the warehouse table.
--
-- Write a single query using FULL OUTER JOIN that identifies:
--   (A) 'missing_in_warehouse'  — rows in source that did NOT make it to warehouse.
--   (B) 'ghost_in_warehouse'    — rows in warehouse with NO matching source record (orphans).
--   (C) 'value_mismatch'        — rows in both, but with different values (amount or status).
--   (D) 'perfect_match'         — rows in both with identical values.
--
-- Return: reconciliation_type, record_id,
--         source_amount, warehouse_amount, amount_delta,
--         source_status, warehouse_status.
--
-- EXTRA:
--   - Also return a SUMMARY row at the end showing count of each reconciliation_type.
--     Hint: UNION ALL with a GROUP BY query on top of the reconciliation result.
--   - The summary rows should have record_id = NULL and amounts = NULL.
--
-- This tests: FULL OUTER JOIN, COALESCE for NULL-safe value comparison,
--             conditional classification logic, and UNION ALL for summary appending.
-- ============================================================

CREATE TABLE source_system (
    record_id INT PRIMARY KEY,
    customer VARCHAR(50),
    amount DECIMAL(10, 2),
    status VARCHAR(20),
    updated_at TIMESTAMP
);

CREATE TABLE warehouse (
    record_id INT PRIMARY KEY,
    customer VARCHAR(50),
    amount DECIMAL(10, 2),
    status VARCHAR(20),
    loaded_at TIMESTAMP
);

INSERT INTO
    source_system
VALUES (
        1,
        'Alice',
        100.00,
        'completed',
        '2024-03-01 10:00'
    ),
    (
        2,
        'Bob',
        250.00,
        'completed',
        '2024-03-01 10:05'
    ),
    (
        3,
        'Carol',
        175.00,
        'pending',
        '2024-03-01 10:10'
    ),
    (
        4,
        'Dave',
        320.00,
        'completed',
        '2024-03-01 10:15'
    ),
    (
        5,
        'Eve',
        89.00,
        'failed',
        '2024-03-01 10:20'
    ),
    (
        6,
        'Frank',
        430.00,
        'completed',
        '2024-03-01 10:25'
    ), -- MISSING in warehouse
    (
        7,
        'Grace',
        55.00,
        'pending',
        '2024-03-01 10:30'
    ), -- MISSING in warehouse
    (
        8,
        'Heidi',
        210.00,
        'completed',
        '2024-03-01 10:35'
    ),
    (
        9,
        'Ivan',
        390.00,
        'completed',
        '2024-03-01 10:40'
    ), -- amount mismatch
    (
        10,
        'Judy',
        145.00,
        'pending',
        '2024-03-01 10:45'
    ), -- status mismatch
    (
        11,
        'Karl',
        500.00,
        'completed',
        '2024-03-01 10:50'
    ),
    (
        12,
        'Laura',
        275.00,
        'failed',
        '2024-03-01 10:55'
    ),
    (
        13,
        'Mallory',
        630.00,
        'completed',
        '2024-03-01 11:00'
    ), -- amount mismatch
    (
        14,
        'Niaj',
        190.00,
        'completed',
        '2024-03-01 11:05'
    ),
    (
        15,
        'Oscar',
        410.00,
        'completed',
        '2024-03-01 11:10'
    );

INSERT INTO
    warehouse
VALUES (
        1,
        'Alice',
        100.00,
        'completed',
        '2024-03-01 10:01'
    ),
    (
        2,
        'Bob',
        250.00,
        'completed',
        '2024-03-01 10:06'
    ),
    (
        3,
        'Carol',
        175.00,
        'pending',
        '2024-03-01 10:11'
    ),
    (
        4,
        'Dave',
        320.00,
        'completed',
        '2024-03-01 10:16'
    ),
    (
        5,
        'Eve',
        89.00,
        'failed',
        '2024-03-01 10:21'
    ),
    (
        8,
        'Heidi',
        210.00,
        'completed',
        '2024-03-01 10:36'
    ),
    (
        9,
        'Ivan',
        399.00,
        'completed',
        '2024-03-01 10:41'
    ), -- amount mismatch (390 vs 399)
    (
        10,
        'Judy',
        145.00,
        'completed',
        '2024-03-01 10:46'
    ), -- status mismatch (pending vs completed)
    (
        11,
        'Karl',
        500.00,
        'completed',
        '2024-03-01 10:51'
    ),
    (
        12,
        'Laura',
        275.00,
        'failed',
        '2024-03-01 10:56'
    ),
    (
        13,
        'Mallory',
        660.00,
        'completed',
        '2024-03-01 11:01'
    ), -- amount mismatch (630 vs 660)
    (
        14,
        'Niaj',
        190.00,
        'completed',
        '2024-03-01 11:06'
    ),
    (
        15,
        'Oscar',
        410.00,
        'completed',
        '2024-03-01 11:11'
    ),
    (
        16,
        'Peggy',
        330.00,
        'completed',
        '2024-03-01 11:15'
    ), -- GHOST: not in source
    (
        17,
        'Quinn',
        720.00,
        'pending',
        '2024-03-01 11:20'
    );
-- GHOST: not in source

-- YOUR QUERY HERE: