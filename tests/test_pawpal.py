from pawpal_system import Task, Pet


def test_task_mark_complete():
    t = Task(title="Test", duration_minutes=10)
    assert not t.completed
    t.mark_complete()
    assert t.completed


def test_pet_add_task_increases_count():
    p = Pet(name="Buddy")
    assert len(p.tasks) == 0
    p.add_task(Task(title="Feed", duration_minutes=5))
    assert len(p.tasks) == 1
