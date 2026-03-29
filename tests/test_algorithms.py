from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def test_sort_tasks_by_due_time():
    owner = Owner(name="TestOwner")
    pet = Pet(name="Buddy")
    t1 = Task(title="Late", duration_minutes=10, due_time="12:30")
    t2 = Task(title="Early", duration_minutes=5, due_time="08:15")
    t3 = Task(title="NoTime", duration_minutes=20)
    pet.add_task(t1)
    pet.add_task(t2)
    pet.add_task(t3)
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_tasks_by_due_time(owner.get_all_tasks())
    titles = [t.title for t in sorted_tasks]
    assert titles == ["Early", "Late", "NoTime"]


def test_recurring_task_creation_on_complete():
    today = date.today()
    t = Task(title="Daily Meds", duration_minutes=5, frequency="daily", due_date=today, due_time="09:00")
    new = t.mark_complete()
    assert t.completed is True
    assert new is not None
    assert new.frequency == "daily"
    assert new.due_date == today + timedelta(days=1)


def test_conflict_detection_flags_overlap():
    # Create a fake schedule with overlapping tasks
    schedule = [
        {"title": "A", "start_time": "09:00", "duration_minutes": 30},
        {"title": "B", "start_time": "09:15", "duration_minutes": 20},
        {"title": "C", "start_time": "10:00", "duration_minutes": 30},
    ]
    scheduler = Scheduler()
    warnings = scheduler.detect_conflicts(schedule)
    assert any("overlaps" in w for w in warnings)
