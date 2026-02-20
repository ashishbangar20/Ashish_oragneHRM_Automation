import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.config_reader import ReadConfig


@allure.feature("Login Module")
@allure.story("Logout Functionality")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_logout(setup):

    driver = setup
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)

    allure.dynamic.title("Verify user can successfully logout")
    allure.dynamic.description(
        "Ensure that a logged-in user can logout successfully "
        "and is redirected back to the login page."
    )

    # ---------- LOGIN ----------
    with allure.step("Login with valid credentials"):
        login.enter_username(ReadConfig.get_username())
        login.enter_password(ReadConfig.get_password())
        login.click_login()

    with allure.step("Wait for dashboard to load"):
        dashboard.wait_for_dashboard_menu()

    # ---------- LOGOUT ----------
    with allure.step("Click logout"):
        dashboard.click_logout()

    with allure.step("Wait for login page to appear"):
        login.wait_for_login_page()

    with allure.step("Verify login page is displayed"):
        assert login.is_login_page_displayed(), \
            "Logout failed - Login page not visible"
