from pawpal.models import Task
from pawpal.scheduler import generate_schedule


def test_generate_schedule_respects_time_limit():
    tasks = [
        Task("Long low", duration_minutes=300, priority="low"),
        Task("Short high", duration_minutes=30, priority="high"),
        Task("Med medium", duration_minutes=60, priority="medium"),
    ]

    scheduled, total = generate_schedule(tasks, available_minutes=60)
    # Only one task should fit into 60 minutes: "Short high"
    assert total == 30
    assert len(scheduled) == 1
    assert scheduled[0]["task"].title == "Short high"


def test_generate_schedule_priority_order():
    tasks = [
        Task("A", duration_minutes=20, priority="medium"),
        Task("B", duration_minutes=20, priority="high"),
        Task("C", duration_minutes=20, priority="low"),
    ]
    scheduled, total = generate_schedule(tasks, available_minutes=60)
    titles = [entry["task"].title for entry in scheduled]
    assert titles == ["B", "A", "C"]
    assert total == 60
