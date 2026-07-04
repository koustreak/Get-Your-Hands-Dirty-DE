-- ============================================================
-- QUESTION 3: Mutual Followers (Symmetric Graph Self JOIN)
-- Difficulty: Advanced | Google / MS DE Level
-- ============================================================
--
-- PROBLEM:
-- Given a social network's follow table (unidirectional),
-- write a query to find ALL pairs of users who MUTUALLY follow each other.
--
-- Requirements:
--   - Return each pair only ONCE: show (user_a, user_b) where user_a < user_b alphabetically.
--   - Also return the number of users that BOTH members of the pair follow
--     (their "common followees" — users both A and B follow, excluding each other).
--   - Only return pairs that have at least 1 common followee.
--   - Order by common_followees DESC, then user_a ASC.
--
-- This tests: self-join on a directed edge table, deduplication of symmetric pairs,
--             and a three-way join to compute commonality.
-- ============================================================

CREATE TABLE follows (
    follower_id VARCHAR(10),
    followee_id VARCHAR(10),
    PRIMARY KEY (follower_id, followee_id)
);

INSERT INTO
    follows
VALUES ('alice', 'bob'),
    ('alice', 'carol'),
    ('alice', 'dave'),
    ('alice', 'eve'),
    ('bob', 'alice'), -- mutual with alice
    ('bob', 'carol'),
    ('bob', 'dave'),
    ('carol', 'alice'), -- mutual with alice
    ('carol', 'bob'), -- mutual with bob
    ('carol', 'eve'),
    ('carol', 'frank'),
    ('dave', 'alice'), -- mutual with alice
    ('dave', 'bob'), -- mutual with bob
    ('dave', 'carol'), -- mutual with carol
    ('dave', 'frank'),
    ('eve', 'alice'), -- mutual with alice
    ('eve', 'carol'), -- mutual with carol
    ('frank', 'carol'), -- mutual with carol
    ('frank', 'dave'), -- mutual with dave
    ('grace', 'alice'),
    ('grace', 'bob'),
    ('alice', 'grace'), -- mutual with grace
    ('bob', 'grace'), -- mutual with grace
    ('heidi', 'frank'),
    ('frank', 'heidi'), -- mutual with heidi
    ('ivan', 'alice'),
    ('ivan', 'bob'),
    ('alice', 'ivan'), -- mutual with ivan
    ('judy', 'eve'),
    ('eve', 'judy');
-- mutual with judy

-- YOUR QUERY HERE:

select
    f1.follower_id user_a,
    f1.followee_id user_b,
    count(DISTINCT f3.followee_id) common_followees
from
    follows f1
    inner join follows f2 on (
        f1.follower_id = f2.followee_id
        and f1.followee_id = f2.follower_id
        and f1.follower_id < f1.followee_id
    )
    inner join follows f3 on (
        f3.follower_id = f1.follower_id
        and f3.followee_id <> f1.followee_id
    )
    inner join follows f4 on (
        f4.follower_id = f1.followee_id
        and f4.followee_id <> f1.follower_id
        and f4.followee_id = f3.followee_id
    )
group by
    f1.follower_id,
    f1.followee_id
having
    count(distinct f3.followee_id) >= 1
order by common_followees desc, f1.follower_id asc