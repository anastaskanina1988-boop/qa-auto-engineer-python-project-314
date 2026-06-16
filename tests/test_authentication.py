"""Тесты входа и выхода."""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    from pages import LoginPage, DashboardPage, PasswordDialog
except ImportError:
    from .pages import LoginPage, DashboardPage, PasswordDialog


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def app_base_url():
    return os.environ.get("APP_BASE_URL", "http://localhost:5173")


def test_successful_login(driver, app_base_url):
    """Проверяем вход."""
    driver.get(app_base_url)
    
    login_page = LoginPage(driver)
    login_page.login("test", "test")
    
    dashboard = DashboardPage(driver)
    assert dashboard.is_loaded()
    assert driver.current_url != app_base_url


def test_login_and_logout(driver, app_base_url):
    """Проверяем вход и выход."""
    driver.get(app_base_url)
    wait = WebDriverWait(driver, 10)
    
    login_page = LoginPage(driver)
    login_page.login("test", "test")
    
    dashboard = DashboardPage(driver)
    assert dashboard.is_loaded()
    
    try:
        dialog = PasswordDialog(driver)
        dialog.click_ok()
    except:
        pass
    
    dashboard.open_profile()
    dashboard.logout()
    
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    assert driver.find_element(By.NAME, "username").is_displayed()
