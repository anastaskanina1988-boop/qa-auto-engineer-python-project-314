try:
    from .admin_list_page import AdminListPage
except ImportError:
    from admin_list_page import AdminListPage


class StatusesPage(AdminListPage):
    link_text = "Task statuses"
    empty_text = "No Task statuses yet."

    def create_status(self, name, slug):
        self.open_create_form()
        self.fill_input_at(0, name)
        self.fill_input_at(1, slug)
        self.save()
        self.wait_for_row(name)

    def rename_status(self, current_name, new_name):
        self.open_row(current_name)
        self.fill_input_at(0, new_name)
        self.save()
        self.open()
        self.wait_for_row(new_name)

    def delete_status(self, name):
        self.open_row(name)
        self.delete()
        self.open()
        self.wait.until(lambda driver: name not in driver.page_source)
