import uuid

try:
    from users_page import UsersPage
except ImportError:
    from .users_page import UsersPage


def unique_email():
    return f"{uuid.uuid4().hex[:8]}@example.com"


def test_users_table_loaded(authenticated_driver):
    users = UsersPage(authenticated_driver).open()

    users.assert_headers("Id", "Email", "First name", "Last name", "Created at")


def test_create_user(authenticated_driver):
    users = UsersPage(authenticated_driver).open()
    email = unique_email()

    users.create_user(email, "Created", "Person")

    assert users.has_text(email)
    assert users.has_text("Created")
    assert users.has_text("Person")


def test_create_user_validates_email(authenticated_driver):
    users = UsersPage(authenticated_driver).open()

    users.open_create_form()
    users.fill_input_at(0, "invalid-email")
    users.fill_input_at(1, "Invalid")
    users.fill_input_at(2, "User")
    users.save()

    users.assert_route("#/users/create")
    users.wait_for_text("Incorrect email format")


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
