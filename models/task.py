from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    description: str | None
    completed: bool
    user_id: int
