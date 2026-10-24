import psycopg

from mentorhub.storage import JsonStorage

storage = JsonStorage("data.json")

with psycopg.connect("dbname=mentorhub") as conn:
    with conn.cursor() as cur:
        goals = storage.load()
        for goal in goals.values():
            cur.execute("SELECT id FROM goals WHERE title = (%s)", (goal.title,))
            res = cur.fetchone()
            if res:
                goal_id = res[0]
            else:
                cur.execute(
                    "INSERT INTO goals (title) VALUES (%s) RETURNING id", (goal.title,)
                )
                goal_id = cur.fetchone()[0]
            for task in goal.tasks:
                cur.execute(
                    "INSERT INTO tasks (title, status_done, goal_id) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (task.title, task.done, goal_id),
                )
            cur.execute(
                "INSERT INTO goal_members (user_id, goal_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (1, goal_id),
            )
