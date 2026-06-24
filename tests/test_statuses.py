import uuid

try:
    from statuses_page import StatusesPage
except ImportError:
    from .statuses_page import StatusesPage


def unique_status(prefix="Status"):
    suffix = uuid.uuid4().hex[:6]
    return f"{prefix} {suffix}", f"status_{suffix}"


def test_statuses_table_loaded(authenticated_driver):
    statuses = StatusesPage(authenticated_driver).open()

    statuses.assert_headers("Id", "Name", "Slug", "Created at")


def test_create_status(authenticated_driver):
    statuses = StatusesPage(authenticated_driver).open()
    name, slug = unique_status()

    statuses.create_status(name, slug)

    assert statuses.has_text(name)


def test_edit_status(authenticated_driver):
    statuses = StatusesPage(authenticated_driver).open()
    name, slug = unique_status()
    updated_name, _ = unique_status("Updated Status")

    statuses.create_status(name, slug)
    statuses.rename_status(name, updated_name)

    assert statuses.has_text(updated_name)


def test_delete_status(authenticated_driver):
    statuses = StatusesPage(authenticated_driver).open()
    name, slug = unique_status()

    statuses.create_status(name, slug)
    statuses.delete_status(name)

    assert not statuses.has_text(name)


def test_delete_all_statuses(authenticated_driver):
    statuses = StatusesPage(authenticated_driver).open()
    name, slug = unique_status()

    statuses.create_status(name, slug)
    statuses.delete_all()

    assert statuses.has_text("No Task statuses yet.")
