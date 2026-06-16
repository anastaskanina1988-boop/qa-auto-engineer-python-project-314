"""Тесты входа и выхода."""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    """Проверяем, что можно войти в приложение."""
    driver.get(app_base_url)
    wait = WebDriverWait(driver, 10)
    
    # Находим поля для входа
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")
    login_btn = driver.find_element(By.TAG_NAME, "button")
    
    # Вводим данные
    username.send_keys("test")
    password.send_keys("test")
    login_btn.click()
    
    # Проверяем, что зашли
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
    assert driver.current_url != app_base_url


def test_login_and_logout(driver, app_base_url):
    """Проверяем вход и выход."""
    driver.get(app_base_url)
    wait = WebDriverWait(driver, 10)
    
    # Вход
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")
    login_btn = driver.find_element(By.TAG_NAME, "button")
    
    username.send_keys("test")
    password.send_keys("test")
    login_btn.click()
    
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
    
    # Закрытие диалога если есть
    try:
        ok = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]")),
            timeout=2
        )
        ok.click()
    except:
        pass
    
    # Выход
    profile = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Jane')]"))
    )
    profile.click()
    
    logout = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.logout"))
    )
    logout.click()
    
    # Проверяем, что вышли
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    assert driver.find_element(By.NAME, "username").is_displayed()
