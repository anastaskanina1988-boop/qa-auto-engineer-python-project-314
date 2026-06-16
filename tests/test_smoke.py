from selenium.webdriver.common.by import By


def test_smoke(driver, app_base_url):
    driver.get(app_base_url)

    inputs = driver.find_elements(By.TAG_NAME, "input")
    buttons = driver.find_elements(By.TAG_NAME, "button")

    assert len(inputs) >= 2
    assert len(buttons) >= 1
