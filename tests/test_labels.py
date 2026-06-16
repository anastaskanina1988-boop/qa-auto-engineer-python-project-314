import uuid

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    from pages import LoginPage
except ImportError:
    from .pages import LoginPage


def test_labels_table_loaded(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(
        By.LINK_TEXT,
        "Labels"
    ).click()

    assert driver.find_element(
        By.XPATH,
        "//th[contains(., 'Name')]"
    )


def test_create_label(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(
        By.LINK_TEXT,
        "Labels"
    ).click()

    driver.find_element(
        By.XPATH,
        '//*[@id="main-content"]/div/div/div[1]/div/a'
    ).click()

    name = f"Label {uuid.uuid4().hex[:6]}"

    driver.find_element(
        By.TAG_NAME,
        "input"
    ).send_keys(name)

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//span[contains(text(), '{name}')]"
            )
        )
    )

    assert name in driver.page_source


def test_edit_label(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(
        By.LINK_TEXT,
        "Labels"
    ).click()

    driver.find_element(
        By.XPATH,
        '//*[@id="main-content"]/div/div/div[1]/div/a'
    ).click()

    name = f"Label {uuid.uuid4().hex[:6]}"

    driver.find_element(
        By.TAG_NAME,
        "input"
    ).send_keys(name)

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//span[contains(text(), '{name}')]"
            )
        )
    )

    driver.find_element(
        By.XPATH,
        f"//span[contains(text(), '{name}')]"
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[aria-label="Save"]')
        )
    )

    input_field = driver.find_element(
        By.TAG_NAME,
        "input"
    )

    input_field.send_keys(Keys.COMMAND, "a")
    input_field.send_keys(Keys.BACKSPACE)
    input_field.send_keys("Updated Label")

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//span[contains(text(), 'Updated Label')]"
            )
        )
    )

    assert driver.find_element(
        By.XPATH,
        "//span[contains(text(), 'Updated Label')]"
    )


def test_delete_label(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(
        By.LINK_TEXT,
        "Labels"
    ).click()

    driver.find_element(
        By.XPATH,
        '//*[@id="main-content"]/div/div/div[1]/div/a'
    ).click()

    name = f"Label {uuid.uuid4().hex[:6]}"

    driver.find_element(
        By.TAG_NAME,
        "input"
    ).send_keys(name)

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//span[contains(text(), '{name}')]"
            )
        )
    )

    driver.find_element(
        By.XPATH,
        f"//span[contains(text(), '{name}')]"
    ).click()

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Delete"]'
    ).click()

    driver.find_element(
        By.LINK_TEXT,
        "Labels"
    ).click()

    assert name not in driver.page_source