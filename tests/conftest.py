"""Shared pytest configuration and fixtures."""

import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

try:
    from login_page import LoginPage
except ImportError:
    from .login_page import LoginPage


@pytest.fixture(scope="session")
def app_base_url():
    """Get the application base URL for local and Hexlet CI runs."""
    base_url = os.environ.get("APP_BASE_URL", "http://localhost:5173")
    if os.environ.get("IMPLEMENTATION") and base_url == "http://localhost:5173":
        return "http://server"
    return base_url


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "login: marks tests as login tests")
    config.addinivalue_line("markers", "logout: marks tests as logout tests")


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def authenticated_driver(driver, app_base_url):
    """Open the app and sign in with the default test user."""
    LoginPage(driver).open(app_base_url).login("test", "test")
    return driver
