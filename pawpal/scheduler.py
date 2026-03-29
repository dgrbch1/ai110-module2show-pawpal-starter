from typing import List, Tuple, Dict
from .models import Task


def generate_schedule(tasks: List[Task], available_minutes: int = 8 * 60, start_hour: int = 8) -> Tuple[List[Dict], int]:
    """Generate a simple daily schedule.

    Strategy: greedy by priority (high -> low), tie-breaker shorter duration first.
    Tasks are scheduled sequentially from `start_hour` until available time is used.

    Returns a tuple: (scheduled_entries, total_scheduled_minutes)
    Each scheduled entry is a dict with `task`, `start_minute`, `start_time`, `explanation`.
    """
    sorted_tasks = sorted(tasks, key=lambda t: (-t.priority_value(), t.duration_minutes))
    scheduled = []
    time_pointer = 0

    for t in sorted_tasks:
        if t.duration_minutes + time_pointer <= available_minutes:
            hour = start_hour + (time_pointer // 60)
            minute = time_pointer % 60
            start_time = f"{hour:02d}:{minute:02d}"
            explanation = (
                f"Chosen (priority={t.priority}) and fits in remaining time ({available_minutes - time_pointer}m)."
            )
            scheduled.append({
                "task": t,
                "start_minute": time_pointer,
                "start_time": start_time,
                "explanation": explanation,
            })
            time_pointer += t.duration_minutes

    return scheduled, time_pointer


def from_dicts(dicts: List[Dict]) -> List[Task]:
    """Helper to convert serializable dicts (like from Streamlit session state) to Task objects."""
    out = []
    for d in dicts:
        out.append(Task(title=d.get("title", ""), duration_minutes=int(d.get("duration_minutes", 0)), priority=d.get("priority", "medium")))
    return out
