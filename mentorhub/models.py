from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    done: bool = False

    def mark_done(self):
        self.done = True


@dataclass
class Goal:
    title: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    @property
    def progress(self) -> int | float:
        progress = 0

        if self.tasks:
            progress = round(
                len([t for t in self.tasks if t.done]) / len(self.tasks) * 100, 1
            )

        return progress

    def get_task_done(self, task_name: str) -> bool:
        for task in self.tasks:
            if task_name == task.title:
                task.mark_done()
                return True
        return False
