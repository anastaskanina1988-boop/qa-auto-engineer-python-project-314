"""Login and logout tests."""

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.password_dialog import PasswordDialog


def test_successful_login(driver, app_base_url):
    LoginPage(driver).open(app_base_url).login("test", "test")

    dashboard = DashboardPage(driver)

    assert dashboard.is_loaded()
    assert driver.current_url != app_base_url
    assert driver.title == "Task manager"
    dashboard.assert_title("Welcome to the administration")
    dashboard.assert_visible_text("Lorem ipsum sic dolor amet...")
    assert dashboard.visible(DashboardPage.PROFILE).is_displayed()


def test_login_and_logout(authenticated_driver):
    dashboard = DashboardPage(authenticated_driver)
    assert dashboard.is_loaded()

    PasswordDialog(authenticated_driver).close_if_present()
    dashboard.open_profile()
    dashboard.logout()

    assert LoginPage(authenticated_driver).visible(LoginPage.USERNAME).is_displayed()
