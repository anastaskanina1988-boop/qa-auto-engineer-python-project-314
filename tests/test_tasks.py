import uuid

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

try:
    from pages import LoginPage
except ImportError:
    from .pages import LoginPage


def test_tasks_table_loaded(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(
        By.LINK_TEXT,
        "Tasks"
    ).click()

    assert "Tasks" in driver.page_source


def test_create_task(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(
        By.LINK_TEXT,
        "Tasks"
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                'a[aria-label="Create"]'
            )
        )
    )

    driver.find_element(
        By.CSS_SELECTOR,
        'a[aria-label="Create"]'
    ).click()

    title = f"Task {uuid.uuid4().hex[:6]}"

    comboboxes = driver.find_elements(
        By.CSS_SELECTOR,
        'div[role="combobox"]'
    )

    # Assignee
    comboboxes[0].click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//li[@role='option']"
            )
        )
    ).click()

    # Title
    driver.find_element(
        By.NAME,
        "title"
    ).send_keys(title)

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

    WebDriverWait(driver, 10).until(
        lambda d: title in d.page_source
    )

    assert title in driver.page_source

def test_edit_task(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    # Открываем задачи
    driver.find_element(
        By.LINK_TEXT,
        "Tasks"
    ).click()

    # Создаем задачу
    driver.find_element(
        By.CSS_SELECTOR,
        'a[aria-label="Create"]'
    ).click()

    title = f"Task {uuid.uuid4().hex[:6]}"

    comboboxes = driver.find_elements(
        By.CSS_SELECTOR,
        'div[role="combobox"]'
    )

    # Assignee
    comboboxes[0].click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//li[@role='option']"
            )
        )
    ).click()

    # Title
    driver.find_element(
        By.NAME,
        "title"
    ).send_keys(title)

    # Status
    comboboxes = driver.find_elements(
        By.CSS_SELECTOR,
        'div[role="combobox"]'
    )

    comboboxes[1].click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//li[@role='option']"
            )
        )
    ).click()

    # Сохраняем
    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

    # Возвращаемся на доску задач
    driver.find_element(
        By.LINK_TEXT,
        "Tasks"
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                'a[aria-label="Edit"]'
            )
        )
    )

    # Открываем последнюю задачу на редактирование
    edit_buttons = driver.find_elements(
        By.CSS_SELECTOR,
        'a[aria-label="Edit"]'
    )

    edit_buttons[-1].click()

    title_input = driver.find_element(
        By.NAME,
        "title"
    )

    print("OLD:", title_input.get_attribute("value"))

    title_input.click()
    title_input.send_keys(Keys.COMMAND + "a")
    title_input.send_keys(Keys.DELETE)

    updated_title = "Updated Task"

    title_input.send_keys(updated_title)

    print("NEW:", title_input.get_attribute("value"))

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

    print("URL:", driver.current_url)

def test_delete_task(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(
        By.LINK_TEXT,
        "Tasks"
    ).click()

    driver.find_element(
        By.CSS_SELECTOR,
        'a[aria-label="Create"]'
    ).click()

    title = f"Task {uuid.uuid4().hex[:6]}"

    comboboxes = driver.find_elements(
        By.CSS_SELECTOR,
        'div[role="combobox"]'
    )

    # Assignee
    comboboxes[0].click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//li[@role='option']"
            )
        )
    ).click()

    # Title
    driver.find_element(
        By.NAME,
        "title"
    ).send_keys(title)

    # Status
    comboboxes = driver.find_elements(
        By.CSS_SELECTOR,
        'div[role="combobox"]'
    )

    comboboxes[1].click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//li[@role='option']"
            )
        )
    ).click()

    # Save
    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

    # Возвращаемся на доску
    driver.find_element(
        By.LINK_TEXT,
        "Tasks"
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                'a[aria-label="Edit"]'
            )
        )
    )

    edit_buttons = driver.find_elements(
        By.CSS_SELECTOR,
        'a[aria-label="Edit"]'
    )

    edit_buttons[-1].click()

    # Delete
    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Delete"]'
    ).click()

    WebDriverWait(driver, 10).until(
        lambda d: "Element deleted" in d.page_source
    )

    assert "Element deleted" in driver.page_source    