"""Page Object классы."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def enter_username(self, username):
        field = self.driver.find_element(By.NAME, "username")
        field.send_keys(username)
    
    def enter_password(self, password):
        field = self.driver.find_element(By.NAME, "password")
        field.send_keys(password)
    
    def click_login(self):
        btn = self.driver.find_element(By.TAG_NAME, "button")
        btn.click()
    
    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()


class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def is_loaded(self):
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
        return True
    
    def open_profile(self):
        profile_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Jane')]")
        profile_btn.click()
    
    def logout(self):
        logout_item = self.driver.find_element(By.CSS_SELECTOR, "li.logout")
        logout_item.click()


class PasswordDialog:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def click_ok(self):
        ok_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]")
        ok_btn.click()
