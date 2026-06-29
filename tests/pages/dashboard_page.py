from selenium.webdriver.common.by import By

from .base_page import BasePage


class DashboardPage(BasePage):
    MAIN = (By.TAG_NAME, "main")
    PROFILE = (By.XPATH, "//button[contains(., 'Jane')]")
    LOGOUT = (By.CSS_SELECTOR, "li.logout")

    def is_loaded(self):
        self.find(self.MAIN)
        return True

    def assert_title(self, title):
        self.visible(
            (
                By.XPATH,
                f"//*[@id='react-admin-title' and normalize-space()='{title}']",
            )
        )

    def assert_visible_text(self, text):
        self.visible((By.XPATH, f"//*[normalize-space()='{text}']"))

    def open_profile(self):
        self.click(self.PROFILE)

    def logout(self):
        self.click(self.LOGOUT)
