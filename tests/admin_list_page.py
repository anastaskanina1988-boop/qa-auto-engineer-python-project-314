from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

try:
    from .base_page import BasePage
except ImportError:
    from base_page import BasePage


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
