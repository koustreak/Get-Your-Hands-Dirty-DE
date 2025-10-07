/*
You are given the list of Facebook friends and the list of Facebook pages that users follow. 
Your task is to create a new recommendation system for Facebook. 
For each Facebook user, find pages that this user doesn't follow but at least one of 
their friends does. Output the user ID and the ID of the page that should be recommended 
to this user.
*/

-- ================================================================
-- TABLE CREATION SCRIPTS
-- ================================================================

-- Drop tables if they exist (for clean slate)
DROP TABLE IF EXISTS users_pages;
DROP TABLE IF EXISTS users_friends;

-- Create users_friends table (stores friendship relationships)
CREATE TABLE users_friends (
    user_id BIGINT,
    friend_id BIGINT,
    PRIMARY KEY (user_id, friend_id)
);

-- Create users_pages table (stores which users follow which pages)
CREATE TABLE users_pages (
    user_id BIGINT,
    page_id BIGINT,
    PRIMARY KEY (user_id, page_id)
);

-- ================================================================
-- SAMPLE DATA INSERTION
-- ================================================================

-- Insert friendship data
INSERT INTO users_friends (user_id, friend_id) VALUES
-- User 1's friends
(1, 2),
(1, 3),
(1, 4),
-- User 2's friends  
(2, 1),
(2, 3),
(2, 5),
-- User 3's friends
(3, 1),
(3, 2),
(3, 4),
(3, 6),
-- User 4's friends
(4, 1),
(4, 3),
(4, 5),
-- User 5's friends
(5, 2),
(5, 4),
(5, 6),
-- User 6's friends
(6, 3),
(6, 5),
-- User 7's friends (isolated user for testing)
(7, 8),
-- User 8's friends
(8, 7);

-- Insert user-page following data
INSERT INTO users_pages (user_id, page_id) VALUES
-- User 1 follows pages
(1, 101),
(1, 102),
-- User 2 follows pages
(2, 102),
(2, 103),
(2, 104),
-- User 3 follows pages
(3, 105),
(3, 106),
-- User 4 follows pages
(4, 103),
(4, 107),
(4, 108),
-- User 5 follows pages
(5, 104),
(5, 105),
(5, 109),
-- User 6 follows pages
(6, 106),
(6, 110),
-- User 7 follows pages
(7, 111),
-- User 8 follows pages
(8, 112),
(8, 113);

-- ================================================================
-- SOLUTION QUERY
-- ================================================================

SELECT DISTINCT
  uf.user_id,
  up_friend.page_id
FROM
  users_friends uf
  JOIN users_pages up_friend
    ON uf.friend_id = up_friend.user_id
WHERE
  NOT EXISTS (
    SELECT 1
    FROM users_pages up_user
    WHERE up_user.user_id = uf.user_id
      AND up_user.page_id = up_friend.page_id
  )
ORDER BY uf.user_id;