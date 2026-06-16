import uuid

try:
    from pages import TasksPage
except ImportError:
    from .pages import TasksPage


def unique_task_title(prefix="Task"):
    return f"{prefix} {uuid.uuid4().hex[:6]}"


def test_tasks_table_loaded(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()

    assert tasks.has_text("Tasks")


def test_create_task(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()
    title = unique_task_title()

    tasks.create_task(title)

    assert tasks.has_text(title)


def test_edit_task(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()
    title = unique_task_title()
    updated_title = unique_task_title("Updated Task")

    tasks.create_task(title, with_status=True)
    tasks.rename_last_task(updated_title)

    assert tasks.has_text(updated_title)


def test_delete_task(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()
    title = unique_task_title()

    tasks.create_task(title, with_status=True)
    tasks.delete_last_task()

    assert tasks.has_text("Element deleted")
