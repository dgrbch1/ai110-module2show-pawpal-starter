from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import date, timedelta, datetime


@dataclass
class Task:
    title: str
    description: str = ""
    duration_minutes: int = 0
    priority: str = "medium"
    frequency: str = "none"  # 'none', 'daily', 'weekly'
    completed: bool = False
    due_date: Optional[date] = None
    due_time: Optional[str] = None  # format 'HH:MM'

    def priority_value(self) -> int:
        """Return an integer weight for priority comparisons."""
        mapping = {"low": 1, "medium": 2, "high": 3}
        return mapping.get(self.priority, 2)

    def mark_complete(self) -> None:
        """Mark this task as completed.

        If the task is recurring (`daily` or `weekly`) and has a `due_date`,
        automatically return a new Task instance scheduled for the next occurrence.
        """
        self.completed = True
        # If recurring, return a new Task instance for the next occurrence
        if self.frequency in ("daily", "weekly") and self.due_date is not None:
            delta = timedelta(days=1) if self.frequency == "daily" else timedelta(weeks=1)
            new_due = self.due_date + delta
            new_task = Task(
                title=self.title,
                description=self.description,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                completed=False,
                due_date=new_due,
                due_time=self.due_time,
            )
            return new_task
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize task to a plain dict for display or storage."""
        return {
            "title": self.title,
            "description": self.description,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "frequency": self.frequency,
            "completed": self.completed,
        }


@dataclass
class Pet:
    name: str
    species: str = "dog"
    preferences: Dict[str, Any] = field(default_factory=dict)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a `Task` to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a `Task` from this pet if present."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self, include_completed: bool = False) -> List[Task]:
        """Return tasks for this pet; optionally exclude completed tasks."""
        if include_completed:
            return list(self.tasks)
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    name: str
    available_minutes: int = 8 * 60
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Attach a `Pet` to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a `Pet` if it belongs to this owner."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self, include_completed: bool = False) -> List[Task]:
        """Collect tasks from all owned pets."""
        tasks: List[Task] = []
        for p in self.pets:
            tasks.extend(p.get_tasks(include_completed=include_completed))
        return tasks


class Scheduler:
    """Scheduler retrieves tasks from an `Owner` or an explicit list and builds a daily plan.

    The scheduler uses a simple greedy algorithm: sort by priority (high->low) then by
    shorter duration; pick tasks until available time is exhausted.
    """

    def __init__(self, owner: Optional[Owner] = None):
        self.owner = owner

    def _collect_tasks(self, tasks: Optional[List[Task]] = None, include_completed: bool = False) -> List[Task]:
        """Helper: get tasks either from provided list or from the owner."""
        if tasks is not None:
            return [t for t in tasks if include_completed or not t.completed]
        if self.owner is not None:
            return self.owner.get_all_tasks(include_completed=include_completed)
        return []

    def filter_tasks(self, pet_name: Optional[str] = None, include_completed: bool = False) -> List[Task]:
        """Return tasks optionally filtered by `pet_name` and completion status.

        If `pet_name` is provided, only tasks for that pet are returned.
        """
        if self.owner is None:
            return []
        if pet_name is None:
            return self.owner.get_all_tasks(include_completed=include_completed)
        pet = next((p for p in self.owner.pets if p.name == pet_name), None)
        if pet is None:
            return []
        return pet.get_tasks(include_completed=include_completed)

    def sort_tasks_by_due_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by their `due_time` string in HH:MM format (earlier first).

        Tasks without `due_time` appear after those with times.
        """
        def key_fn(t: Task):
            if t.due_time:
                try:
                    dt = datetime.strptime(t.due_time, "%H:%M")
                    return (0, dt.hour * 60 + dt.minute)
                except Exception:
                    return (0, 24 * 60)
            return (1, 24 * 60)

        return sorted(tasks, key=key_fn)

    def sort_schedule_by_time(self, schedule: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort schedule entries by their `start_time` field (HH:MM)."""
        def parse_start(s: Dict[str, Any]):
            st = s.get("start_time")
            if not st:
                return 24 * 60
            try:
                dt = datetime.strptime(st, "%H:%M")
                return dt.hour * 60 + dt.minute
            except Exception:
                return 24 * 60

        return sorted(schedule, key=parse_start)

    def detect_conflicts(self, schedule: List[Dict[str, Any]]) -> List[str]:
        """Lightweight conflict detection: return warnings for overlapping tasks.

        Strategy: convert `start_time` to minutes and check interval overlaps.
        """
        warnings: List[str] = []
        intervals: List[tuple] = []  # (start_minute, end_minute, title)

        for e in schedule:
            st = e.get("start_time")
            dur = e.get("duration_minutes", 0)
            title = e.get("title", "<task>")
            if not st:
                continue
            try:
                dt = datetime.strptime(st, "%H:%M")
                start_min = dt.hour * 60 + dt.minute
            except Exception:
                continue
            end_min = start_min + dur
            for s0, e0, t0 in intervals:
                # overlap check
                if not (end_min <= s0 or start_min >= e0):
                    warnings.append(f"Conflict: '{title}' overlaps with '{t0}' at {st}.")
            intervals.append((start_min, end_min, title))

        return warnings

    def generate_schedule(self, tasks: Optional[List[Task]] = None, available_minutes: Optional[int] = None, start_hour: int = 8) -> List[Dict[str, Any]]:
        """Generate a schedule and return a list of entries with human-friendly fields.

        Each entry contains: `title`, `duration_minutes`, `priority`, `start_time`, and `explanation`.
        """
        if available_minutes is None:
            available_minutes = self.owner.available_minutes if self.owner is not None else 0

        candidates = self._collect_tasks(tasks)
        # Sort by priority (desc), then by duration (asc)
        candidates.sort(key=lambda t: (-t.priority_value(), t.duration_minutes))

        scheduled: List[Dict[str, Any]] = []
        time_pointer = 0

        for t in candidates:
            if t.duration_minutes + time_pointer <= available_minutes:
                hour = start_hour + (time_pointer // 60)
                minute = time_pointer % 60
                start_time = f"{hour:02d}:{minute:02d}"
                explanation = f"Selected (priority={t.priority}) — fits remaining {available_minutes - time_pointer}m."
                scheduled.append({
                    "title": t.title,
                    "duration_minutes": t.duration_minutes,
                    "priority": t.priority,
                    "start_time": start_time,
                    "explanation": explanation,
                    "task": t,
                })
                time_pointer += t.duration_minutes

        return scheduled

    def pretty_print(self, schedule: List[Dict[str, Any]]) -> None:
        """Print a readable schedule to stdout."""
        if not schedule:
            print("No tasks scheduled.")
            return
        print("Today's Schedule:")
        for entry in schedule:
            print(f"- {entry['start_time']} | {entry['title']} ({entry['duration_minutes']}m) — {entry['priority']}\n  {entry['explanation']}")

