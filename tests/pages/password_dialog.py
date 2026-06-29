from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from .base_page import BasePage


class PasswordDialog(BasePage):
    OK_BUTTON = (By.XPATH, "//button[contains(., 'OK')]")

    def close_if_present(self):
        try:
            self.click(self.OK_BUTTON)
        except TimeoutException:
            pass
