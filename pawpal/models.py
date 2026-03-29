from dataclasses import dataclass
from typing import Dict


@dataclass
class Owner:
    name: str
    available_minutes: int = 8 * 60


@dataclass
class Pet:
    name: str
    species: str = "dog"


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"

    def priority_value(self) -> int:
        mapping = {"low": 1, "medium": 2, "high": 3}
        return mapping.get(self.priority, 2)

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
        }
