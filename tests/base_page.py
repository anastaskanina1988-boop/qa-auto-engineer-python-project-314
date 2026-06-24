import platform

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


DEFAULT_TIMEOUT = 10


class BasePage:
    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def click(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator)).click()

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def fill(self, locator, value):
        field = self.visible(locator)
        self.replace_text(field, value)
        return field

    def replace_text(self, field, value):
        shortcut = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
        field.click()
        field.clear()
        field.send_keys(shortcut + "a")
        field.send_keys(Keys.BACKSPACE)
        field.send_keys(value)
        if field.get_attribute("value") != value:
            self.driver.execute_script(
                """
                const element = arguments[0];
                const value = arguments[1];
                const previousValue = element.value;
                element.value = value;
                const tracker = element._valueTracker;
                if (tracker) {
                    tracker.setValue(previousValue);
                }
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                """,
                field,
                value,
            )

    def wait_for_text(self, text):
        self.wait.until(lambda driver: text in driver.page_source)

    def has_text(self, text):
        return text in self.driver.page_source
