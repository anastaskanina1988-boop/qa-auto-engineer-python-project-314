from selenium.webdriver.common.by import By

from .base_page import BasePage


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
