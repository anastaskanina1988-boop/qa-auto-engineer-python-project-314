try:
    from .admin_list_page import AdminListPage
except ImportError:
    from admin_list_page import AdminListPage


class UsersPage(AdminListPage):
    link_text = "Users"
    empty_text = "No Users yet."

    def create_user(self, email, first_name="Test", last_name="User"):
        self.open_create_form()
        self.fill_input_at(0, email)
        self.fill_input_at(1, first_name)
        self.fill_input_at(2, last_name)
        self.save()
        self.wait_for_row(email)

    def update_first_name(self, email, first_name):
        self.open_row(email)
        self.fill_input_at(1, first_name)
        self.save()
        self.open()
        self.wait_for_text(first_name)

    def delete_user(self, email):
        self.open_row(email)
        self.delete()
        self.open()
        self.wait.until(lambda driver: email not in driver.page_source)
