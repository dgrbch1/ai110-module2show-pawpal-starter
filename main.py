from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date


def demo():
    owner = Owner(name="Jordan", available_minutes=180)

    pet1 = Pet(name="Mochi", species="dog")
    pet2 = Pet(name="Kiko", species="cat")

    # Add tasks with due_time and due_date to demonstrate sorting, conflicts, and recurring
    today = date.today()
    t1 = Task(title="Morning walk", description="Short walk around block", duration_minutes=30, priority="high", frequency="daily", due_date=today, due_time="09:00")
    t2 = Task(title="Feed breakfast", description="Dry food", duration_minutes=10, priority="medium", due_date=today, due_time="08:30")
    t3 = Task(title="Give meds", description="Pill with water", duration_minutes=5, priority="high", due_date=today, due_time="09:00")
    t4 = Task(title="Grooming", description="Brush fur", duration_minutes=40, priority="low", due_date=today, due_time="11:00")

    pet1.add_task(t1)
    pet1.add_task(t2)
    pet2.add_task(t3)
    pet2.add_task(t4)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner=owner)
    # Demonstrate filtering and sorting
    pet1.add_task(t1)
    pet1.add_task(t2)
    pet2.add_task(t3)
    pet2.add_task(t4)

    print("\nAll tasks unsorted:")
    for t in owner.get_all_tasks():
        print(t.to_dict())

    print("\nTasks sorted by due_time:")
    sorted_tasks = scheduler.sort_tasks_by_due_time(owner.get_all_tasks())
    for t in sorted_tasks:
        print(t.title, t.due_time)

    print("\nTasks filtered for Mochi:")
    mochis = scheduler.filter_tasks(pet_name="Mochi")
    for t in mochis:
        print(t.title, t.due_time)

    # Generate schedule and detect conflicts
    schedule = scheduler.generate_schedule()
    scheduler.pretty_print(schedule)
    conflicts = scheduler.detect_conflicts(schedule)
    if conflicts:
        print("\nConflicts detected:")
        for c in conflicts:
            print(c)

    # Mark a recurring task complete and auto-create next occurrence
    print("\nMarking 'Morning walk' complete (recurring):")
    new_task = t1.mark_complete()
    print("Completed:", t1.completed)
    if new_task:
        print("New recurring task created for:", new_task.due_date)
        pet1.add_task(new_task)

    print("\nFinal task list for Mochi:")
    for t in pet1.get_tasks(include_completed=True):
        print(t.to_dict())


if __name__ == "__main__":
    demo()
