import psycopg

from mentorhub.models import Goal, Task
from mentorhub.storage_base import Storage


class PostgresStorage(Storage):
    def save(self, goals: dict[str, Goal]) -> None:
        with psycopg.connect("dbname=mentorhub") as conn:
            with conn.cursor() as cur:
                for goal in goals.values():
                    cur.execute(
                        """ INSERT INTO goals (title)
                                VALUES (%s)
                                ON CONFLICT (title)
                                DO UPDATE SET title = EXCLUDED.title
                                RETURNING id""",
                        (goal.title,),
                    )
                    goal_id = cur.fetchone()[0]
                    for task in goal.tasks:
                        cur.execute(
                            """ INSERT INTO tasks (title, status_done, goal_id, completed_at)
                                VALUES (%s, %s, %s, CASE WHEN %s THEN NOW() ELSE NULL END)
                                ON CONFLICT (goal_id, title)
                                DO UPDATE SET status_done = EXCLUDED.status_done,
                                              completed_at = CASE 
                                              WHEN tasks.status_done = FALSE
                                              AND EXCLUDED.status_done = TRUE
                                              THEN NOW()
                                              WHEN EXCLUDED.status_done = FALSE
                                              THEN NULL
                                              ELSE tasks.completed_at 
                                              END""",
                            (task.title, task.done, goal_id, task.done),
                        )
                    cur.execute(
                        """ INSERT INTO goal_members (user_id, goal_id)
                                VALUES (%s, %s)
                                ON CONFLICT (user_id, goal_id)
                                DO NOTHING""",
                        (1, goal_id),
                    )

    def load(self) -> dict[str, Goal]:
        with psycopg.connect("dbname=mentorhub") as conn:
            with conn.cursor() as cur:
                goals = {}
                cur.execute("""SELECT g.id, g.title, t.title, t.status_done
                             FROM goals g
                             JOIN goal_members gm ON gm.goal_id = g.id
                             LEFT JOIN tasks t ON t.goal_id = g.id
                             WHERE gm.user_id = 1""")
                res = cur.fetchall()
                for row in res:
                    if row[1] not in goals:
                        goals[row[1]] = Goal(row[1], [])
                    if row[2] is not None:
                        goals[row[1]].tasks.append(Task(row[2], row[3]))
                return goals
