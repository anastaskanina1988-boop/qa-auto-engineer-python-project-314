from selenium.webdriver.common.by import By

try:
    from .base_page import BasePage
except ImportError:
    from base_page import BasePage


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
