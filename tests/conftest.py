"""Shared pytest configuration and fixtures."""

import os
import pytest


@pytest.fixture(scope="session")
def app_base_url():
    """Get the application base URL from environment variable."""
    return os.environ.get("APP_BASE_URL", "http://localhost:5173")


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "login: marks tests as login tests")
    config.addinivalue_line("markers", "logout: marks tests as logout tests")
from selenium import webdriver


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()