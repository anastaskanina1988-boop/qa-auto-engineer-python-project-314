"""Page Object."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def enter_username(self, username):
        self.driver.find_element(By.NAME, "username").send_keys(username)
    
    def enter_password(self, password):
        self.driver.find_element(By.NAME, "password").send_keys(password)
    
    def click_login(self):
        self.driver.find_element(By.TAG_NAME, "button").click()
    
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
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Jane')]").click()
    
    def logout(self):
        self.driver.find_element(By.CSS_SELECTOR, "li.logout").click()


class PasswordDialog:
    def __init__(self, driver):
        self.driver = driver
    
    def click_ok(self):
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]").click()
