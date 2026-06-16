import os

from selenium import webdriver
from selenium.webdriver.common.by import By


def test_smoke():
    driver = webdriver.Chrome()

    try:
        driver.get(os.environ["APP_BASE_URL"])

        inputs = driver.find_elements(By.TAG_NAME, "input")
        buttons = driver.find_elements(By.TAG_NAME, "button")

        assert len(inputs) >= 2
        assert len(buttons) >= 1

    finally:
        driver.quit()