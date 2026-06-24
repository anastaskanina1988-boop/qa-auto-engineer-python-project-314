from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

try:
    from .admin_list_page import AdminListPage
except ImportError:
    from admin_list_page import AdminListPage


class TasksPage(AdminListPage):
    link_text = "Tasks"

    EDIT_LINKS = (By.CSS_SELECTOR, 'a[aria-label="Edit"]')
    TITLE = (By.NAME, "title")
    COMBOBOXES = (By.CSS_SELECTOR, 'div[role="combobox"]')
    OPTION = (By.XPATH, "//li[@role='option']")
    FILTER_ASSIGNEE = (
        By.XPATH,
        "//label[normalize-space()='Assignee']"
        "/ancestor::div[contains(@class, 'MuiFormControl-root')][1]",
    )
    FILTER_STATUS = (
        By.XPATH,
        "//label[normalize-space()='Status']"
        "/ancestor::div[contains(@class, 'MuiFormControl-root')][1]",
    )
    FILTER_LABEL = (
        By.XPATH,
        "//label[normalize-space()='Label']"
        "/ancestor::div[contains(@class, 'MuiFormControl-root')][1]",
    )

    def verify_filters_visible(self):
        self.open()
        filters = {
            self.FILTER_ASSIGNEE: "Assignee",
            self.FILTER_STATUS: "Status",
            self.FILTER_LABEL: "Label",
        }

        for locator, expected_text in filters.items():
            element = self.wait.until(EC.visibility_of_element_located(locator))
            if expected_text not in element.text:
                return False

        return True

    def create_task(self, title, with_status=False):
        self.open_create_form()
        self.select_combobox_option(0)
        self.fill(self.TITLE, title)

        if with_status:
            self.select_combobox_option(1)

        self.save()
        self.open()
        self.wait_for_text(title)

    def rename_task(self, current_title, new_title):
        self.open()
        self.open_edit_form(current_title)
        self.fill(self.TITLE, new_title)
        self.save()
        self.open()
        self.wait_for_text(new_title)

    def delete_last_task(self):
        self.open()
        self.open_last_edit_form()
        self.delete()
        self.wait_for_text("Element deleted")

    def open_last_edit_form(self):
        self.wait.until(EC.presence_of_element_located(self.EDIT_LINKS))
        edit_links = self.driver.find_elements(*self.EDIT_LINKS)
        edit_links[-1].click()
        self.find(self.SAVE)

    def open_edit_form(self, title):
        self.click(
            (
                By.XPATH,
                "//*[normalize-space()="
                f"'{title}']/ancestor::*[@role='button'][1]"
                "//a[@aria-label='Edit']",
            )
        )
        self.find(self.SAVE)

    def select_combobox_option(self, index):
        comboboxes = self.wait.until(
            lambda driver: driver.find_elements(*self.COMBOBOXES)
        )
        comboboxes[index].click()
        self.click(self.OPTION)
