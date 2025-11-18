-- test_fixture.sql
-- This SQL file contains 5 predefined habits + completions over 4 weeks for testing purposes.


INSERT INTO habits (id, name, description, periodicity, created_at) VALUES
(1, 'Reading', 'Read for 20 minutes every day', 'daily', '2025-10-20 08:00:00'),
(2, 'Meditation', '10 minutes of mindfulness', 'daily', '2025-10-20 08:05:00'),
(3, 'Jogging', 'Run once a week', 'weekly', '2025-10-20 08:10:00'),
(4, 'Clean apartment', 'Thorough cleaning once a week', 'weekly', '2025-10-20 08:15:00'),
(5, 'Tax documents', 'Sort at the end of the month', 'monthly', '2025-10-20 08:20:00');

-- Reading (daily): Test data for 4 weeks at a time (always completed)
INSERT INTO completions (habit_id, completed_at) VALUES
(1, '2025-10-20 19:00:00'),
(1, '2025-10-21 19:00:00'),
(1, '2025-10-22 19:00:00'),
(1, '2025-10-23 19:00:00'),
(1, '2025-10-24 19:00:00'),
(1, '2025-10-25 19:00:00'),
(1, '2025-10-26 19:00:00'),
(1, '2025-10-27 19:00:00'),
(1, '2025-10-28 19:00:00'),
(1, '2025-10-29 19:00:00'),
(1, '2025-10-30 19:00:00'),
(1, '2025-10-31 19:00:00'),
(1, '2025-11-01 19:00:00'),
(1, '2025-11-02 19:00:00'),
(1, '2025-11-03 19:00:00'),
(1, '2025-11-04 19:00:00'),
(1, '2025-11-05 19:00:00'),
(1, '2025-11-06 19:00:00'),
(1, '2025-11-07 19:00:00'),
(1, '2025-11-08 19:00:00'),
(1, '2025-11-09 19:00:00'),
(1, '2025-11-10 19:00:00'),
(1, '2025-11-11 19:00:00'),
(1, '2025-11-12 19:00:00'),
(1, '2025-11-13 19:00:00'),
(1, '2025-11-14 19:00:00'),
(1, '2025-11-15 19:00:00'),
(1, '2025-11-16 19:00:00');

-- Meditation (daily): Test data for 4 weeks in a row (not done every day)
INSERT INTO completions (habit_id, completed_at) VALUES
(2, '2025-10-20 07:30:00'),
(2, '2025-10-22 07:30:00'),
(2, '2025-10-24 07:30:00'),
(2, '2025-10-26 07:30:00'),
(2, '2025-10-28 07:30:00'),
(2, '2025-10-30 07:30:00'),
(2, '2025-11-01 07:30:00'),
(2, '2025-11-03 07:30:00'),
(2, '2025-11-05 07:30:00'),
(2, '2025-11-07 07:30:00'),
(2, '2025-11-09 07:30:00'),
(2, '2025-11-11 07:30:00'),
(2, '2025-11-13 07:30:00'),
(2, '2025-11-15 07:30:00'),
(2, '2025-11-16 07:30:00');

-- Jogging (weekly): Test data for 4 weeks (completed once per week)
INSERT INTO completions (habit_id, completed_at) VALUES
(3, '2025-10-21 18:00:00'),
(3, '2025-10-28 18:00:00'),
(3, '2025-11-04 18:00:00'),
(3, '2025-11-11 18:00:00');

-- Clean apartment (weekly): Test data for 4 weeks (completed once per week)
INSERT INTO completions (habit_id, completed_at) VALUES
(4, '2025-10-23 10:00:00'),
(4, '2025-10-30 10:00:00'),
(4, '2025-11-06 10:00:00'),
(4, '2025-11-13 10:00:00');

-- Tax documents (monthly): Test data for 4 weeks (completed once every 4 weeks)
INSERT INTO completions (habit_id, completed_at) VALUES
(5, '2025-10-31 20:00:00');
