import uuid

try:
    from pages import TasksPage
except ImportError:
    from .pages import TasksPage


def unique_task_title(prefix="Task"):
    return f"{prefix} {uuid.uuid4().hex[:6]}"


def test_tasks_table_loaded(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()

    tasks.assert_route("#/tasks")
    tasks.assert_browser_title("Task manager")
    tasks.assert_page_title("Tasks")
    tasks.assert_active_menu_item("Tasks")
    tasks.assert_create_link("#/tasks/create")
    tasks.assert_filter_labels("Assignee", "Status", "Label")
    tasks.assert_visible_texts(
        "Draft", "To Review", "To Be Fixed", "To Publish", "Published"
    )
    tasks.assert_kanban_column_contains("Draft", "Task 11")
    tasks.assert_kanban_column_contains("To Review", "Task 2")
    tasks.assert_kanban_column_contains("To Be Fixed", "Task 1")
    tasks.assert_kanban_column_contains("To Publish", "Task 3")
    tasks.assert_kanban_column_contains("Published", "Task 4")
    tasks.assert_kanban_card_in_column("1", "11", "Task 11")
    tasks.assert_kanban_card_in_column("2", "2", "Task 2")
    tasks.assert_kanban_card_in_column("3", "1", "Task 1")
    tasks.assert_kanban_card_in_column("4", "3", "Task 3")
    tasks.assert_kanban_card_in_column("5", "4", "Task 4")


def test_create_task(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()
    title = unique_task_title()

    tasks.create_task(title, with_status=True)

    assert tasks.has_text(title)
    tasks.assert_kanban_column_contains("Published", title)


def test_edit_task(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()
    title = unique_task_title()
    updated_title = unique_task_title("Updated Task")

    tasks.create_task(title, with_status=True)
    tasks.rename_task(title, updated_title)

    assert tasks.has_text(updated_title)
    tasks.assert_kanban_column_contains("Published", updated_title)


def test_delete_task(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()
    title = unique_task_title()

    tasks.create_task(title, with_status=True)
    tasks.delete_last_task()

    assert tasks.has_text("Element deleted")
