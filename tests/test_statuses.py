import uuid

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    from pages import LoginPage
except ImportError:
    from .pages import LoginPage


def test_statuses_table_loaded(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(By.LINK_TEXT, "Task statuses").click()

    assert driver.find_element(
        By.XPATH,
        "//th[contains(., 'Name')]"
    )


    assert driver.find_element(
        By.XPATH,
        "//th[contains(., 'Slug')]"
    )


def test_create_status(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(By.LINK_TEXT, "Task statuses").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//th[contains(., 'Name')]")
        )
    )

    driver.find_element(
        By.XPATH,
        '//*[@id="main-content"]/div/div/div[1]/div/a'
    ).click()

    name = f"Status {uuid.uuid4().hex[:6]}"
    slug = f"status_{uuid.uuid4().hex[:6]}"

    inputs = driver.find_elements(By.TAG_NAME, "input")

    inputs[0].send_keys(name)
    inputs[1].send_keys(slug)

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

    assert name in driver.page_source


from selenium.webdriver.common.keys import Keys


def test_edit_status(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(
        By.LINK_TEXT,
        "Task statuses"
    ).click()

    driver.find_element(
        By.XPATH,
        '//*[@id="main-content"]/div/div/div[1]/div/a'
    ).click()

    name = f"Status {uuid.uuid4().hex[:6]}"
    slug = f"status_{uuid.uuid4().hex[:6]}"

    inputs = driver.find_elements(By.TAG_NAME, "input")

    inputs[0].send_keys(name)
    inputs[1].send_keys(slug)

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

    inputs = driver.find_elements(By.TAG_NAME, "input")

    inputs[0].send_keys(Keys.COMMAND, "a")
    inputs[0].send_keys(Keys.BACKSPACE)
    inputs[0].send_keys("Updated Status")

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//span[contains(text(), 'Updated Status')]"
            )
        )
    )

    assert driver.find_element(
        By.XPATH,
        "//span[contains(text(), 'Updated Status')]"
    )


def test_delete_status(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(By.LINK_TEXT, "Task statuses").click()

    driver.find_element(
        By.XPATH,
        '//*[@id="main-content"]/div/div/div[1]/div/a'
    ).click()

    name = f"Status {uuid.uuid4().hex[:6]}"
    slug = f"status_{uuid.uuid4().hex[:6]}"

    inputs = driver.find_elements(By.TAG_NAME, "input")

    inputs[0].send_keys(name)
    inputs[1].send_keys(slug)

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

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
        "Task statuses"
    ).click()

    assert name not in driver.page_source


def test_delete_all_statuses(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(
        By.LINK_TEXT,
        "Task statuses"
    ).click()

    driver.find_element(
        By.CSS_SELECTOR,
        'input[aria-label="Select all"]'
    ).click()

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Delete"]'
    ).click()

    WebDriverWait(driver, 10).until(
        lambda d: "No Task statuses yet." in d.page_source
    )

    assert "No Task statuses yet." in driver.page_source