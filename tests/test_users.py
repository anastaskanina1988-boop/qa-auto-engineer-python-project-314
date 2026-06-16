
import uuid
from selenium.webdriver.common.by import By
try:
    from pages import LoginPage
except ImportError:
    from .pages import LoginPage

def test_users_table_loaded(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(By.LINK_TEXT, "Users").click()

    assert driver.find_element(By.XPATH, "//th[contains(., 'Email')]")
    assert driver.find_element(By.XPATH, "//th[contains(., 'First name')]")
    assert driver.find_element(By.XPATH, "//th[contains(., 'Last name')]")

def test_create_user(driver, app_base_url):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(By.LINK_TEXT, "Users").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//th[contains(., 'Email')]")
        )
    )

    driver.find_element(
        By.XPATH,
        '//*[@id="main-content"]/div/div/div[1]/div/a'
    ).click()

    email = f"{uuid.uuid4().hex[:8]}@example.com"

    inputs = driver.find_elements(By.TAG_NAME, "input")

    inputs[0].send_keys(email)
    inputs[1].send_keys("Test")
    inputs[2].send_keys("User")

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

    assert email in driver.page_source


def test_edit_user(driver, app_base_url):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(By.LINK_TEXT, "Users").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//th[contains(., 'Email')]")
        )
    )

    driver.find_element(
        By.XPATH,
        '//*[@id="main-content"]/div/div/div[1]/div/a'
    ).click()

    email = f"{uuid.uuid4().hex[:8]}@example.com"

    inputs = driver.find_elements(By.TAG_NAME, "input")

    inputs[0].send_keys(email)
    inputs[1].send_keys("Test")
    inputs[2].send_keys("User")

    driver.find_element(
        By.XPATH,
        '//button[@aria-label="Save"]'
    ).click()

    driver.find_element(
        By.XPATH,
        f"//span[contains(text(), '{email}')]"
    ).click()

    inputs = driver.find_elements(By.TAG_NAME, "input")

    inputs[1].clear()
    inputs[1].send_keys("Updated")

    driver.find_element(
        By.XPATH,
        '//button[@aria-label="Save"]'
    ).click()

    assert "Updated" in driver.page_source  

def test_delete_user(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(By.LINK_TEXT, "Users").click()

    driver.find_element(
        By.XPATH,
        '//*[@id="main-content"]/div/div/div[1]/div/a'
    ).click()

    email = f"{uuid.uuid4().hex[:8]}@example.com"

    inputs = driver.find_elements(By.TAG_NAME, "input")

    inputs[0].send_keys(email)
    inputs[1].send_keys("Delete")
    inputs[2].send_keys("User")

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Save"]'
    ).click()

    assert email in driver.page_source

    driver.find_element(
        By.XPATH,
        f"//span[contains(text(), '{email}')]"
    ).click()

    driver.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Delete"]'
    ).click()
    
    driver.find_element(By.LINK_TEXT, "Users").click()
    assert email not in driver.page_source      