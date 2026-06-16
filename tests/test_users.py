try:
    from pages import LoginPage
except ImportError:
    from .pages import LoginPage

from selenium.webdriver.common.by import By


def test_users_table_loaded(driver, app_base_url):
    driver.get(app_base_url)

    login_page = LoginPage(driver)
    login_page.login("test", "test")

    driver.find_element(By.LINK_TEXT, "Users").click()

    assert driver.find_element(By.XPATH, "//th[contains(., 'Email')]")
    assert driver.find_element(By.XPATH, "//th[contains(., 'First name')]")
    assert driver.find_element(By.XPATH, "//th[contains(., 'Last name')]")