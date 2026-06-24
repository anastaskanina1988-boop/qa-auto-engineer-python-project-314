import uuid

try:
    from tasks_page import TasksPage
except ImportError:
    from .tasks_page import TasksPage


def unique_task_title(prefix="Task"):
    return f"{prefix} {uuid.uuid4().hex[:6]}"


def test_tasks_table_loaded(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()

    tasks.assert_route("#/tasks")
    tasks.assert_browser_title("Task manager")
    tasks.assert_page_title("Tasks")
    tasks.assert_active_menu_item("Tasks")
    tasks.assert_create_link("#/tasks/create")
    tasks.assert_refresh_button_hidden()
    assert tasks.verify_filters_visible()
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


def test_create_task_with_details(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()
    title = unique_task_title("Detailed Task")
    content = f"Details {uuid.uuid4().hex[:6]}"

    tasks.create_task_with_details(title, content)

    tasks.assert_kanban_column_contains("Published", title)
    tasks.open_show_form_by_title(title)
    tasks.assert_visible_texts("john@google.com", title, content, "bug")


def test_filter_tasks_by_status(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()

    tasks.filter_by_status("Draft")

    tasks.assert_kanban_card_visible("11", "Task 11")
    tasks.assert_kanban_card_not_visible("2")


def test_filter_tasks_by_assignee(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()

    tasks.filter_by_assignee("john@google.com")

    tasks.assert_kanban_card_visible("11", "Task 11")
    tasks.assert_kanban_card_not_visible("12")


def test_filter_tasks_by_label(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()

    tasks.filter_by_label("bug")

    tasks.assert_kanban_card_visible("7", "Task 7")
    tasks.assert_kanban_card_not_visible("11")


def test_show_task_details(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()

    tasks.open_show_form("11")

    tasks.assert_visible_texts(
        "john@google.com",
        "Task 11",
        "Description of task 11",
        "bug",
        "feature",
        "enhancement",
    )


def test_tasks_sorted_by_index_in_columns(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()

    tasks.assert_kanban_column_card_order("1", "11", "5", "6")
    tasks.assert_kanban_column_card_order("2", "2", "12", "7")
    tasks.assert_kanban_column_card_order("3", "1", "13", "8")
    tasks.assert_kanban_column_card_order("4", "3", "14", "9")
    tasks.assert_kanban_column_card_order("5", "4", "15", "10")


def test_move_task_to_another_column(authenticated_driver):
    tasks = TasksPage(authenticated_driver).open()

    tasks.move_card_to_next_column("11")

    tasks.assert_kanban_card_not_in_column("1", "11")
    tasks.assert_kanban_card_in_column("2", "11", "Task 11")


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
