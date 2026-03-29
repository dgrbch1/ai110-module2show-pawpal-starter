import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner & Pets")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

# Owner name (sync with stored Owner)
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name

st.markdown("### Pets")
col_a, col_b = st.columns(2)
with col_a:
    new_pet_name = st.text_input("New pet name", value="")
with col_b:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"], index=0)

if st.button("Add pet"):
    if new_pet_name:
        pet = Pet(name=new_pet_name, species=new_pet_species)
        st.session_state.owner.add_pet(pet)
        st.success(f"Added pet {new_pet_name}")

if st.session_state.owner.pets:
    st.write("Current pets and tasks:")
    for p in st.session_state.owner.pets:
        st.markdown(f"**{p.name}** ({p.species})")
        if p.tasks:
            st.table([t.to_dict() for t in p.tasks])
        else:
            st.caption("No tasks for this pet yet.")

st.divider()

st.subheader("Add Task")
st.caption("Add a task and assign it to a pet.")

pet_options = [p.name for p in st.session_state.owner.pets] if st.session_state.owner.pets else []
selected_pet = None
if pet_options:
    selected_pet_name = st.selectbox("Pet", pet_options)
    selected_pet = next((p for p in st.session_state.owner.pets if p.name == selected_pet_name), None)
else:
    st.info("Add a pet first to assign tasks.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if not selected_pet:
        st.error("Please add and select a pet before adding a task.")
    else:
        t = Task(title=task_title, duration_minutes=int(duration), priority=priority)
        selected_pet.add_task(t)
        st.success(f"Added task '{task_title}' to {selected_pet.name}")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule from your pets' pending tasks.")

if st.button("Generate schedule"):
    try:
        scheduler = Scheduler(owner=st.session_state.owner)
    except Exception as e:
        st.error(f"Scheduler not available: {e}")
    else:
        available_minutes = st.number_input("Available minutes today", min_value=1, max_value=24 * 60, value=st.session_state.owner.available_minutes)
        include_completed = st.checkbox("Include completed tasks", value=False)
        pet_filter = st.selectbox("Filter by pet (optional)", ["All"] + [p.name for p in st.session_state.owner.pets])

        tasks_for_schedule = None
        if pet_filter != "All":
            tasks_for_schedule = scheduler.filter_tasks(pet_name=pet_filter, include_completed=include_completed)
        else:
            tasks_for_schedule = scheduler.filter_tasks(pet_name=None, include_completed=include_completed)

        scheduled = scheduler.generate_schedule(tasks=tasks_for_schedule, available_minutes=available_minutes)
        if not scheduled:
            st.info("No tasks fit in the available time.")
        else:
            # Sort schedule by start_time for clear presentation
            scheduled = scheduler.sort_schedule_by_time(scheduled)
            rows = []
            for entry in scheduled:
                rows.append({
                    "title": entry["title"],
                    "duration_minutes": entry["duration_minutes"],
                    "priority": entry["priority"],
                    "start_time": entry["start_time"],
                    "explanation": entry["explanation"],
                })

            # Detect conflicts and show warnings
            conflicts = scheduler.detect_conflicts(scheduled)
            if conflicts:
                for c in conflicts:
                    st.warning(c)
            else:
                st.success("No conflicts detected.")

            st.write("Generated schedule:")
            st.table(rows)
            total = sum(r["duration_minutes"] for r in rows)
            st.markdown(f"**Total scheduled minutes:** {total}")
