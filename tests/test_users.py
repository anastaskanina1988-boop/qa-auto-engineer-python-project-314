import uuid

try:
    from pages import UsersPage
except ImportError:
    from .pages import UsersPage


def unique_email():
    return f"{uuid.uuid4().hex[:8]}@example.com"


def test_users_table_loaded(authenticated_driver):
    users = UsersPage(authenticated_driver).open()

    users.assert_headers("Email", "First name", "Last name")


def test_create_user(authenticated_driver):
    users = UsersPage(authenticated_driver).open()
    email = unique_email()

    users.create_user(email)

    assert users.has_text(email)


def test_edit_user(authenticated_driver):
    users = UsersPage(authenticated_driver).open()
    email = unique_email()

    users.create_user(email)
    users.update_first_name(email, "Updated")

    assert users.has_text("Updated")


def test_delete_user(authenticated_driver):
    users = UsersPage(authenticated_driver).open()
    email = unique_email()

    users.create_user(email, first_name="Delete")
    users.delete_user(email)

    assert not users.has_text(email)


def test_delete_all_users(authenticated_driver):
    users = UsersPage(authenticated_driver).open()
    email = unique_email()

    users.create_user(email)
    users.delete_all()

    assert users.has_text("No Users yet.")
