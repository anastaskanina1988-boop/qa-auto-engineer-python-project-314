"""Login and logout tests."""

try:
    from pages import DashboardPage, LoginPage, PasswordDialog
except ImportError:
    from .pages import DashboardPage, LoginPage, PasswordDialog


def test_successful_login(driver, app_base_url):
    LoginPage(driver).open(app_base_url).login("test", "test")

    dashboard = DashboardPage(driver)

    assert dashboard.is_loaded()
    assert dashboard.visible(DashboardPage.PROFILE).is_displayed()



def test_login_and_logout(authenticated_driver):
    dashboard = DashboardPage(authenticated_driver)
    assert dashboard.is_loaded()

    PasswordDialog(authenticated_driver).close_if_present()
    dashboard.open_profile()
    dashboard.logout()

    assert LoginPage(authenticated_driver).visible(LoginPage.USERNAME).is_displayed()
