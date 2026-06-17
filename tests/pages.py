"""Page objects shared by the Selenium tests."""

import platform

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


DEFAULT_TIMEOUT = 10


class BasePage:
    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def click(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator)).click()

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def fill(self, locator, value):
        field = self.visible(locator)
        self.replace_text(field, value)
        return field

    def replace_text(self, field, value):
        shortcut = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
        field.click()
        field.clear()
        field.send_keys(shortcut + "a")
        field.send_keys(Keys.BACKSPACE)
        field.send_keys(value)
        if field.get_attribute("value") != value:
            self.driver.execute_script(
                """
                const element = arguments[0];
                const value = arguments[1];
                const previousValue = element.value;
                element.value = value;
                const tracker = element._valueTracker;
                if (tracker) {
                    tracker.setValue(previousValue);
                }
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                """,
                field,
                value,
            )

    def wait_for_text(self, text):
        self.wait.until(lambda driver: text in driver.page_source)

    def has_text(self, text):
        return text in self.driver.page_source


class LoginPage(BasePage):
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    SUBMIT = (By.TAG_NAME, "button")

    def open(self, base_url):
        self.driver.get(base_url)
        self.visible(self.USERNAME)
        return self

    def login(self, username, password):
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.SUBMIT)


class DashboardPage(BasePage):
    MAIN = (By.TAG_NAME, "main")
    PROFILE = (By.XPATH, "//button[contains(., 'Jane')]")
    LOGOUT = (By.CSS_SELECTOR, "li.logout")

    def is_loaded(self):
        self.find(self.MAIN)
        return True

    def open_profile(self):
        self.click(self.PROFILE)

    def logout(self):
        self.click(self.LOGOUT)


class PasswordDialog(BasePage):
    OK_BUTTON = (By.XPATH, "//button[contains(., 'OK')]")

    def close_if_present(self):
        try:
            self.click(self.OK_BUTTON)
        except TimeoutException:
            pass


class AdminListPage(BasePage):
    link_text = None
    empty_text = None

    CREATE = (By.CSS_SELECTOR, 'a[aria-label="Create"]')
    DELETE = (By.CSS_SELECTOR, 'button[aria-label="Delete"]')
    SAVE = (By.CSS_SELECTOR, 'button[aria-label="Save"]')
    SELECT_ALL = (By.CSS_SELECTOR, "span.select-all")

    def open(self):
        self.click((By.LINK_TEXT, self.link_text))
        return self

    def open_create_form(self):
        self.click(self.CREATE)
        self.find(self.SAVE)

    def save(self):
        self.click(self.SAVE)

    def delete(self):
        self.click(self.DELETE)

    def input_at(self, index):
        return self.wait.until(
            lambda driver: (
                inputs[index]
                if len(inputs := driver.find_elements(By.TAG_NAME, "input")) > index
                else False
            )
        )

    def fill_input_at(self, index, value):
        field = self.input_at(index)
        self.replace_text(field, value)
        return field

    def row_text(self, text):
        return (By.XPATH, f"//span[contains(., '{text}')]")

    def wait_for_row(self, text):
        self.find(self.row_text(text))

    def open_row(self, text):
        self.click(self.row_text(text))
        self.find(self.SAVE)

    def assert_headers(self, *headers):
        for header in headers:
            self.find((By.XPATH, f"//th[contains(., '{header}')]"))

    def assert_page_title(self, title):
        self.visible(
            (
                By.XPATH,
                f"//*[@id='react-admin-title' and normalize-space()='{title}']",
            )
        )

    def assert_route(self, route):
        self.wait.until(lambda driver: driver.current_url.endswith(route))

    def assert_browser_title(self, title):
        self.wait.until(EC.title_is(title))

    def assert_active_menu_item(self, text):
        self.visible(
            (
                By.XPATH,
                "//a[contains(@class, 'RaMenuItemLink-active') "
                f"and normalize-space()='{text}']",
            )
        )

    def assert_create_link(self, route):
        self.visible(
            (
                By.XPATH,
                f"//a[@aria-label='Create' and contains(@href, '{route}')]",
            )
        )

    def assert_filter_labels(self, *labels):
        for label in labels:
            self.visible((By.XPATH, f"//label[normalize-space()='{label}']"))

    def assert_visible_texts(self, *texts):
        for text in texts:
            self.visible((By.XPATH, f"//*[normalize-space()='{text}']"))

    def assert_kanban_column_contains(self, column, card_title):
        self.visible(
            (
                By.XPATH,
                "//div[./h6[normalize-space()="
                f"'{column}'] and .//*[normalize-space()='{card_title}']]",
            )
        )

    def assert_kanban_card_in_column(self, column_id, card_id, card_title):
        self.visible(
            (
                By.XPATH,
                f"//*[@data-rfd-droppable-id='{column_id}']"
                f"//*[@data-rfd-draggable-id='{card_id}' "
                f"and .//*[normalize-space()='{card_title}']]",
            )
        )

    def delete_all(self):
        self.open()
        self.click(self.SELECT_ALL)
        self.delete()
        self.wait_for_text(self.empty_text)


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
        self.wait_for_text(first_name)

    def delete_user(self, email):
        self.open_row(email)
        self.delete()
        self.open()
        self.wait.until(lambda driver: email not in driver.page_source)


class TasksPage(AdminListPage):
    link_text = "Tasks"

    EDIT_LINKS = (By.CSS_SELECTOR, 'a[aria-label="Edit"]')
    TITLE = (By.NAME, "title")
    COMBOBOXES = (By.CSS_SELECTOR, 'div[role="combobox"]')
    OPTION = (By.XPATH, "//li[@role='option']")

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
