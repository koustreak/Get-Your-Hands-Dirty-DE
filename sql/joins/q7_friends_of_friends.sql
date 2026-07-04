-- ============================================================
-- QUESTION 7: Friends You May Know (2nd Degree Graph JOIN)
-- Difficulty: Super Advanced | Google / MS DE Level
-- ============================================================
--
-- PROBLEM:
-- Given a symmetric friendship table (if A-B exists, B-A also exists),
-- implement a simplified "People You May Know" feature.
--
-- Recommend user pairs (A, B) where:
--   1. A and B are NOT already direct friends.
--   2. A and B have at least 2 mutual friends in common.
--   3. A ≠ B.
--
-- Return: user_a, user_b, mutual_friend_count, mutual_friend_names (comma-separated, sorted)
-- Order by mutual_friend_count DESC, user_a ASC, user_b ASC.
--
-- EXTRA CONSTRAINT: Exclude any pair where user_a or user_b has been BLOCKED
--   by the other (see blocked_users table).
--
-- This tests: multi-hop self JOIN on an edge table, aggregation over join results,
--             exclusion via anti-join against two separate conditions, STRING_AGG.
-- ============================================================

CREATE TABLE friendships (
    user_a VARCHAR(20),
    user_b VARCHAR(20),
    since DATE,
    PRIMARY KEY (user_a, user_b),
    CHECK (user_a < user_b) -- canonical ordering to avoid duplicates
);

CREATE TABLE blocked_users (
    blocker VARCHAR(20),
    blocked VARCHAR(20),
    PRIMARY KEY (blocker, blocked)
);

INSERT INTO
    friendships
VALUES ('alice', 'bob', '2023-01-10'),
    (
        'alice',
        'carol',
        '2023-02-15'
    ),
    ('alice', 'dave', '2023-03-20'),
    (
        'alice',
        'frank',
        '2023-04-05'
    ),
    (
        'alice',
        'grace',
        '2023-05-10'
    ),
    ('bob', 'carol', '2023-01-12'),
    ('bob', 'dave', '2023-03-25'),
    ('bob', 'eve', '2023-06-01'),
    ('bob', 'heidi', '2023-07-15'),
    ('carol', 'dave', '2023-02-20'),
    ('carol', 'eve', '2023-06-10'),
    (
        'carol',
        'frank',
        '2023-04-12'
    ),
    ('dave', 'grace', '2023-05-22'),
    ('dave', 'heidi', '2023-07-20'),
    ('eve', 'frank', '2023-08-01'),
    ('eve', 'grace', '2023-05-30'),
    ('frank', 'ivan', '2023-09-01'),
    (
        'grace',
        'heidi',
        '2023-07-25'
    ),
    ('grace', 'ivan', '2023-09-10'),
    ('heidi', 'ivan', '2023-09-15'),
    ('heidi', 'judy', '2023-10-01'),
    ('ivan', 'judy', '2023-10-05'),
    ('judy', 'karl', '2023-11-01'),
    ('ivan', 'karl', '2023-11-10'),
    ('frank', 'karl', '2023-11-15');

INSERT INTO
    blocked_users
VALUES ('eve', 'alice'), -- eve blocked alice, so (alice, eve) pair must be excluded
    ('karl', 'carol');
-- karl blocked carol

-- YOUR QUERY HERE: