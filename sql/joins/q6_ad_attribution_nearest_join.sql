-- ============================================================
-- QUESTION 6: Event Attribution (Nearest Prior Event JOIN)
-- Difficulty: Super Advanced | Google / MS DE Level
-- ============================================================
--
-- PROBLEM:
-- You have two event streams:
--   1. ad_clicks: records when a user clicked on an advertisement.
--   2. purchases: records when a user made a purchase.
--
-- Attribution Rule (Last-Touch):
--   - A purchase is "attributed" to the MOST RECENT ad_click by the same user
--     that happened WITHIN 7 days BEFORE the purchase.
--   - If multiple ad_clicks qualify, attribute to the closest one in time.
--   - If NO ad_click qualifies, the purchase is "organic" (unattributed).
--
-- Write a query that returns:
--   purchase_id, user_id, purchase_time, purchase_amount,
--   attributed_click_id, click_time, ad_campaign,
--   minutes_between_click_and_purchase (NULL if organic),
--   is_organic (TRUE/FALSE).
--
-- Bonus constraint: A single ad_click can only be credited ONCE.
--   If two purchases are within 7 days of the same click,
--   only the CHRONOLOGICALLY FIRST purchase gets the attribution.
--   The second purchase falls back to the next eligible click, or becomes organic.
--
-- This tests: non-equi JOIN with time-range conditions, ranking within join results,
--             deduplication of join output, and multi-priority resolution.
-- ============================================================

CREATE TABLE ad_clicks (
    click_id INT PRIMARY KEY,
    user_id INT,
    click_time TIMESTAMP,
    ad_campaign VARCHAR(50)
);

CREATE TABLE purchases (
    purchase_id INT PRIMARY KEY,
    user_id INT,
    purchase_time TIMESTAMP,
    purchase_amount DECIMAL(10, 2)
);

INSERT INTO
    ad_clicks
VALUES (
        1,
        101,
        '2024-03-01 10:00',
        'Spring Sale'
    ),
    (
        2,
        101,
        '2024-03-05 14:00',
        'Email Blast'
    ),
    (
        3,
        101,
        '2024-03-10 09:00',
        'Retargeting'
    ),
    (
        4,
        102,
        '2024-03-02 11:00',
        'Spring Sale'
    ),
    (
        5,
        102,
        '2024-03-08 16:00',
        'Social Ad'
    ),
    (
        6,
        103,
        '2024-03-01 08:00',
        'Spring Sale'
    ),
    (
        7,
        103,
        '2024-03-15 12:00',
        'Retargeting'
    ),
    (
        8,
        104,
        '2024-03-01 09:00',
        'Email Blast'
    ),
    (
        9,
        104,
        '2024-03-20 10:00',
        'Social Ad'
    ),
    (
        10,
        105,
        '2024-03-05 15:00',
        'Spring Sale'
    ),
    (
        11,
        105,
        '2024-03-12 11:00',
        'Email Blast'
    ),
    (
        12,
        106,
        '2024-03-01 10:00',
        'Social Ad'
    ),
    (
        13,
        107,
        '2024-03-10 09:00',
        'Retargeting'
    ),
    (
        14,
        107,
        '2024-03-18 14:00',
        'Spring Sale'
    );

INSERT INTO
    purchases
VALUES (
        1,
        101,
        '2024-03-08 15:00',
        149.99
    ), -- User 101: clicks on 1(Mar1), 2(Mar5) -- nearest click is 2
    (
        2,
        101,
        '2024-03-09 10:00',
        79.99
    ), -- User 101: click 2(Mar5) already used by purchase 1, falls to click 1 or organic?
    (
        3,
        101,
        '2024-03-11 18:00',
        220.00
    ), -- User 101: click 3(Mar10) is nearest and unused
    (
        4,
        102,
        '2024-03-14 10:00',
        349.00
    ), -- User 102: click 5(Mar8) is within 7 days
    (
        5,
        102,
        '2024-03-03 09:00',
        99.00
    ), -- User 102: only click 4(Mar2) within 7 days
    (
        6,
        103,
        '2024-03-14 11:00',
        59.99
    ), -- User 103: click 6(Mar1) is 13 days prior (outside window), click 7(Mar15) is AFTER purchase -- organic
    (
        7,
        103,
        '2024-03-17 10:00',
        189.00
    ), -- User 103: click 7(Mar15) is 2 days prior -- attributed
    (
        8,
        104,
        '2024-03-10 09:00',
        420.00
    ), -- User 104: click 8(Mar1) is 9 days prior (outside), click 9(Mar20) is after -- organic
    (
        9,
        105,
        '2024-03-15 14:00',
        310.00
    ), -- User 105: click 11(Mar12) is 3 days prior -- attributed
    (
        10,
        105,
        '2024-03-16 10:00',
        75.00
    ), -- User 105: click 11 already used, click 10(Mar5) is 11 days prior (outside) -- organic
    (
        11,
        106,
        '2024-02-25 12:00',
        200.00
    ), -- User 106: purchase BEFORE any click -- organic
    (
        12,
        107,
        '2024-03-15 11:00',
        130.00
    ), -- User 107: click 13(Mar10) is 5 days prior -- attributed
    (
        13,
        107,
        '2024-03-22 09:00',
        95.00
    ), -- User 107: click 14(Mar18) is 4 days prior -- attributed
    (
        14,
        108,
        '2024-03-10 10:00',
        50.00
    );
-- User 108: No clicks at all -- organic

-- YOUR QUERY HERE: