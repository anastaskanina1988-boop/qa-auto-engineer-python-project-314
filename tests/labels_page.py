try:
    from .admin_list_page import AdminListPage
except ImportError:
    from admin_list_page import AdminListPage


class LabelsPage(AdminListPage):
    link_text = "Labels"

    def create_label(self, name):
        self.open_create_form()
        self.fill_input_at(0, name)
        self.save()
        self.wait_for_row(name)

    def rename_label(self, current_name, new_name):
        self.open_row(current_name)
        self.fill_input_at(0, new_name)
        self.save()
        self.open()
        self.wait_for_row(new_name)

    def delete_label(self, name):
        self.open_row(name)
        self.delete()
        self.open()
        self.wait.until(lambda driver: name not in driver.page_source)
