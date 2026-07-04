-- ============================================================
-- QUESTION 2: Overlapping Meeting Rooms (Non-Equi Self JOIN)
-- Difficulty: Advanced | Google / MS DE Level
-- ============================================================
--
-- PROBLEM:
-- A company has a single shared conference room.
-- Find all PAIRS of bookings that overlap in time.
-- Two bookings overlap if one starts before the other ends.
--
-- Rules:
--   - Do NOT return the same pair twice (A,B) and (B,A).
--   - A booking that ends exactly when another starts does NOT count as an overlap.
--   - Return: booking_id_1, user_1, booking_id_2, user_2,
--             overlap_start (the later of the two start times),
--             overlap_end   (the earlier of the two end times),
--             overlap_minutes (duration of the overlap in minutes).
--
-- Order by overlap_minutes DESC.
-- ============================================================

CREATE TABLE room_bookings (
    booking_id INT PRIMARY KEY,
    user_name VARCHAR(50),
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

INSERT INTO
    room_bookings
VALUES (
        1,
        'Alice',
        '2024-03-01 09:00',
        '2024-03-01 10:00'
    ),
    (
        2,
        'Bob',
        '2024-03-01 09:30',
        '2024-03-01 11:00'
    ), -- overlaps with 1
    (
        3,
        'Carol',
        '2024-03-01 10:00',
        '2024-03-01 11:00'
    ), -- touches 1 (no overlap), overlaps 2
    (
        4,
        'Dave',
        '2024-03-01 10:30',
        '2024-03-01 12:30'
    ), -- overlaps 2, 3
    (
        5,
        'Eve',
        '2024-03-01 12:00',
        '2024-03-01 13:00'
    ), -- overlaps 4
    (
        6,
        'Frank',
        '2024-03-01 13:30',
        '2024-03-01 14:30'
    ),
    (
        7,
        'Grace',
        '2024-03-01 14:00',
        '2024-03-01 15:00'
    ), -- overlaps 6
    (
        8,
        'Heidi',
        '2024-03-01 14:15',
        '2024-03-01 16:00'
    ), -- overlaps 6, 7
    (
        9,
        'Ivan',
        '2024-03-01 09:00',
        '2024-03-01 17:00'
    ), -- overlaps everything!
    (
        10,
        'Judy',
        '2024-03-01 16:30',
        '2024-03-01 17:30'
    ),
    (
        11,
        'Karl',
        '2024-03-02 09:00',
        '2024-03-02 10:00'
    ),
    (
        12,
        'Laura',
        '2024-03-02 09:45',
        '2024-03-02 10:45'
    ), -- overlaps 11
    (
        13,
        'Mallory',
        '2024-03-02 10:00',
        '2024-03-02 11:00'
    ), -- touches 11, overlaps 12
    (
        14,
        'Niaj',
        '2024-03-02 11:00',
        '2024-03-02 12:00'
    ),
    (
        15,
        'Oscar',
        '2024-03-02 11:30',
        '2024-03-02 13:00'
    ), -- overlaps 14
    (
        16,
        'Peggy',
        '2024-03-02 12:45',
        '2024-03-02 14:00'
    ), -- overlaps 15
    (
        17,
        'Quinn',
        '2024-03-02 09:00',
        '2024-03-02 12:00'
    ), -- overlaps 11, 12, 13, 14, 15
    (
        18,
        'Romeo',
        '2024-03-02 13:00',
        '2024-03-02 14:00'
    ), -- touches 15, overlaps 16
    (
        19,
        'Sybil',
        '2024-03-02 13:30',
        '2024-03-02 15:00'
    ), -- overlaps 16, 18
    (
        20,
        'Trent',
        '2024-03-02 14:30',
        '2024-03-02 15:30'
    );
-- overlaps 16, 19

-- YOUR QUERY HERE:

select
    rb.booking_id AS booking_id_1,
    rb.user_name AS user_1,
    rb1.booking_id AS booking_id_2,
    rb1.user_name AS user_2,
    GREATEST(rb.start_time, rb1.start_time) overlap_starts,
    least(rb.end_time, rb1.end_time) overlap_ends,
    extract(
        epoch
        from (
                least(rb.end_time, rb1.end_time) - GREATEST(rb.start_time, rb1.start_time)
            )
    ) / 60.0::FLOAT as overlap_minutes
from
    room_bookings rb
    inner join room_bookings rb1 on (
        rb.end_time > rb1.start_time
        and rb.booking_id < rb1.booking_id
        and rb.start_time < rb1.end_time
    )
order by rb.booking_id asc