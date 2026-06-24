from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

try:
    from .admin_list_page import AdminListPage
except ImportError:
    from admin_list_page import AdminListPage


class TasksPage(AdminListPage):
    link_text = "Tasks"

    EDIT_LINKS = (By.CSS_SELECTOR, 'a[aria-label="Edit"]')
    TITLE = (By.NAME, "title")
    CONTENT = (By.NAME, "content")
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

    def filter_by_status(self, status):
        self.select_filter_option(1, status, "status_id")

    def filter_by_assignee(self, assignee):
        self.select_filter_option(0, assignee, "assignee_id")

    def filter_by_label(self, label):
        self.select_filter_option(2, label, "label_id")

    def select_filter_option(self, index, option_text, filter_key):
        comboboxes = self.wait.until(
            lambda driver: (
                elements
                if len(elements := driver.find_elements(*self.COMBOBOXES)) > index
                else False
            )
        )
        comboboxes[index].click()
        option = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//li[@role='option' and normalize-space()='{option_text}']",
                )
            )
        )
        self.driver.execute_script("arguments[0].click();", option)
        self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        self.wait.until(
            lambda driver: all(
                combobox.get_attribute("aria-expanded") == "false"
                for combobox in driver.find_elements(*self.COMBOBOXES)
            )
        )
        self.wait.until(lambda driver: filter_key in driver.current_url)

    def assert_kanban_card_visible(self, card_id, card_title):
        self.visible(
            (
                By.XPATH,
                f"//*[@data-rfd-draggable-id='{card_id}' "
                f"and .//*[normalize-space()='{card_title}']]",
            )
        )

    def assert_kanban_card_not_visible(self, card_id):
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, f"[data-rfd-draggable-id='{card_id}']")
            )
        )

    def create_task(self, title, with_status=False):
        self.open_create_form()
        self.select_combobox_option(0)
        self.fill(self.TITLE, title)

        if with_status:
            self.select_combobox_option(1)

        self.save()
        self.open()
        self.wait_for_text(title)

    def create_task_with_details(self, title, content):
        self.open_create_form()
        self.select_combobox_option_by_text(0, "john@google.com")
        self.fill(self.TITLE, title)
        self.fill(self.CONTENT, content)
        self.select_combobox_option_by_text(1, "Published")
        self.select_combobox_option_by_text(2, "bug")
        self.driver.execute_script("arguments[0].click();", self.find(self.SAVE))
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

    def open_show_form(self, card_id):
        self.click(
            (
                By.XPATH,
                f"//*[@data-rfd-draggable-id='{card_id}']"
                "//a[@aria-label='Show']",
            )
        )
        self.wait.until(lambda driver: f"#/tasks/{card_id}/show" in driver.current_url)

    def move_card_to_next_column(self, card_id):
        card = self.visible((By.XPATH, f"//*[@data-rfd-draggable-id='{card_id}']"))
        self.driver.execute_script("arguments[0].focus();", card)
        card.send_keys(Keys.SPACE)
        card.send_keys(Keys.ARROW_RIGHT)
        card.send_keys(Keys.SPACE)

    def open_show_form_by_title(self, title):
        self.click(
            (
                By.XPATH,
                "//*[normalize-space()="
                f"'{title}']/ancestor::*[@role='button'][1]"
                "//a[@aria-label='Show']",
            )
        )
        self.wait.until(lambda driver: "/show" in driver.current_url)

    def select_combobox_option(self, index):
        comboboxes = self.wait.until(
            lambda driver: driver.find_elements(*self.COMBOBOXES)
        )
        comboboxes[index].click()
        self.click(self.OPTION)

    def select_combobox_option_by_text(self, index, option_text):
        comboboxes = self.wait.until(
            lambda driver: (
                elements
                if len(elements := driver.find_elements(*self.COMBOBOXES)) > index
                else False
            )
        )
        comboboxes[index].click()
        option = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//li[@role='option' and normalize-space()='{option_text}']",
                )
            )
        )
        self.driver.execute_script("arguments[0].click();", option)
