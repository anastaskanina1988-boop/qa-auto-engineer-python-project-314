"""Shared pytest configuration and fixtures."""

import os

import pytest
from selenium import webdriver

try:
    from pages import LoginPage
except ImportError:
    from .pages import LoginPage


@pytest.fixture(scope="session")
def app_base_url():
    """Get the application base URL from environment variable."""
    return os.environ.get("APP_BASE_URL", "http://localhost:5173")


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "login: marks tests as login tests")
    config.addinivalue_line("markers", "logout: marks tests as logout tests")


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def authenticated_driver(driver, app_base_url):
    """Open the app and sign in with the default test user."""
    LoginPage(driver).open(app_base_url).login("test", "test")
    return driver
