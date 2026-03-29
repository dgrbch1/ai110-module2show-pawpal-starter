# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

This version includes a few algorithmic improvements:

- Sorting: tasks can be sorted by `due_time` (HH:MM) for clearer presentation.
- Filtering: you can filter tasks by pet and by completion status.
- Recurring tasks: marking a `daily` or `weekly` task complete will auto-create the next occurrence.
- Conflict detection: the scheduler performs lightweight overlap checks and returns warnings when tasks overlap.

These features keep the app simple while making everyday scheduling more useful.

## Testing PawPal+

Run the automated tests with:

```bash
python -m pytest
```

The test suite covers:
- Core task and pet behaviors (adding tasks, marking complete).
- Scheduler behaviors: priority-based scheduling, time-based sorting, recurring task creation, and conflict detection.

Confidence: ★★★★☆ (4/5) — tests cover main flows and basic edge cases; further tests could validate complex overlapping windows and multi-day planning.

## Features

- Add and manage multiple `Pet` objects per `Owner`.
- Create tasks with `duration`, `priority`, optional `due_time` and `due_date`, and `frequency` (`daily`/`weekly`).
- Sorting: tasks can be sorted by `due_time` for clear daily ordering.
- Filtering: filter tasks by pet and by completion status in both CLI and UI.
- Recurrence: completing a `daily` or `weekly` task auto-creates the next occurrence.
- Conflict detection: lightweight overlap checking with warnings presented to the user.

## 📸 Demo

To include a screenshot of the app, replace the path below with your screenshot file:

<a href="/course_images/ai110/your_screenshot_name.png" target="_blank"><img src='/course_images/ai110/your_screenshot_name.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>
