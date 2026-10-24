WITH stats AS (
SELECT users.name AS user_name, 
       COUNT(tasks.id) AS total_tasks, 
       COUNT(tasks.id) FILTER (WHERE completed_at >= date_trunc('week', NOW()) 
                       AND completed_at < date_trunc('week', NOW()) + INTERVAL '1 week' 
                       AND tasks.status_done = TRUE) AS completed_week
FROM users
JOIN goal_members ON users.id = goal_members.user_id JOIN goals ON goal_members.goal_id = goals.id JOIN tasks ON goals.id = tasks.goal_id
WHERE name = 'Alex'
GROUP BY users.id
)

SELECT user_name, total_tasks, completed_week, ROUND(completed_week * 100.0 / NULLIF(total_tasks, 0), 1) AS progress_percent
FROM stats;